"""Magic-square regression: all nine input pairs, exact probabilities and real shots.

MUT selects a source file; default is sibling fixed.py. No source rewriting.
"""
from functools import lru_cache
import os
from pathlib import Path
import runpy
import subprocess
import sys
import unittest
import numpy as np

@lru_cache(None)
def target():
    return runpy.run_path(os.environ.get('MUT',str(Path(__file__).with_name('fixed.py'))),run_name='apr_target')

def independently_wins(bits,x,y):
    # The output's left two bits form Alice's row, right two Bob's column.
    a0,a1,b0,b1=map(int,bits)
    alice=[a0,a1,a0 ^ a1]       # even row parity
    bob=[b0,b1,1 ^ b0 ^ b1]   # odd column parity
    return alice[y-1]==bob[x-1]

class TestMagicSquare(unittest.TestCase):
    def test_decoder_all_outcomes_and_inputs(self):
        m=target()
        counts={format(i,'04b'):i+1 for i in range(16)}
        for x in (1,2,3):
            for y in (1,2,3):
                expected=sum(freq for bits,freq in counts.items() if independently_wins(bits,x,y))
                self.assertEqual(m['interpret_magic_square_ideal'](counts,x,y),(expected,sum(counts.values())-expected))

    def test_exact_perfect_strategy_for_all_nine_inputs(self):
        from qiskit.quantum_info import Statevector
        m=target()
        psi=m['define_initial_state']()
        expected=np.zeros(16); expected[[3,6,9,12]]=[0.5,-0.5,-0.5,0.5]
        np.testing.assert_allclose(psi,expected,atol=1e-12)
        operators=m['define_unitary_operators']()
        loss_probabilities=[]
        for x in (1,2,3):
            for y in (1,2,3):
                qc=m['create_quantum_circuit'](psi,operators,x,y)
                self.assertEqual((qc.num_qubits,qc.num_clbits),(4,4))
                probabilities=Statevector.from_instruction(qc.remove_final_measurements(inplace=False)).probabilities()
                self.assertAlmostEqual(float(sum(probabilities)),1,places=12)
                loss=sum(p for i,p in enumerate(probabilities) if not independently_wins(format(i,'04b'),x,y))
                loss_probabilities.append(float(loss))
        print('EXACT_LOSS_PROBABILITIES (x,y lexicographic):',loss_probabilities)
        np.testing.assert_allclose(loss_probabilities,np.zeros(9),atol=1e-12,rtol=0,
                                   err_msg='The ideal magic-square strategy must win every input pair.')

    def test_real_simulator_shots_for_all_nine_inputs(self):
        # Isolate native Aer crashes so exact-math checks still report their outcomes.
        p=subprocess.run([sys.executable,'-X','utf8',str(Path(__file__).resolve()),'--simulate'],
                         capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=90)
        print(p.stdout,p.stderr,flush=True)
        if p.returncode:
            raise RuntimeError('SIMULATOR_PROCESS_ERROR: exit='+str(p.returncode)+' (0x'+format(p.returncode & 0xffffffff,'08X')+')')

    def run_simulator_checks(self):
        m=target()
        psi=m['define_initial_state']()
        operators=m['define_unitary_operators']()
        lost=[]
        for x in (1,2,3):
            for y in (1,2,3):
                counts=m['execute_circuit_ideal'](m['create_quantum_circuit'](psi,operators,x,y),shots=128)
                self.assertEqual(sum(counts.values()),128)
                independent=sum(freq for bits,freq in counts.items() if not independently_wins(bits,x,y))
                self.assertEqual(m['interpret_magic_square_ideal'](counts,x,y),(128-independent,independent))
                lost.append(independent)
        print('SAMPLED_LOSSES (128 shots each):',lost)
        self.assertEqual(lost,[0]*9,'Every ideal sample must satisfy the game constraints.')

if __name__=='__main__':
    if '--simulate' in sys.argv:
        TestMagicSquare().run_simulator_checks()
    else:
        unittest.main()
