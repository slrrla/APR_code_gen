"""Standalone behavioral regression test. MUT selects source; default: sibling fixed.py."""
import os
from pathlib import Path
import runpy
import unittest
import numpy as np

def load_target():
    return runpy.run_path(os.environ.get("MUT", str(Path(__file__).with_name("fixed.py"))), run_name="__main__")

class TestPulseFrequencyWorkaround(unittest.TestCase):
    def test_full_sweep_and_modulated_waveforms(self):
        from qiskit.pulse import Play, DriveChannel
        from qiskit.pulse.transforms import inline_subroutines
        m = load_target()
        self.assertEqual(len(m['spec01_scheds']), 71)
        frequencies = np.asarray(m['spec_freqs_GHz'])
        center = round(m['center_frequency'][0], -8)/1e9
        np.testing.assert_allclose(frequencies, np.linspace(center-0.15,center+0.15,71), atol=1e-12)
        envelope = m['spec_pulse'].get_waveform().samples
        times = np.arange(len(envelope))*m['dt']
        for freq,schedule in zip(frequencies,m['spec01_scheds']):
            instructions = inline_subroutines(schedule).instructions
            self.assertFalse(any(type(inst).__name__ in ('SetFrequency','ShiftFrequency') for _,inst in instructions))
            drives = [(t,inst) for t,inst in instructions if isinstance(inst,Play) and inst.channel == DriveChannel(0)]
            self.assertGreaterEqual(len(drives),1)
            t,drive = drives[0]
            self.assertEqual(t,0)
            expected = envelope * np.exp(2j*np.pi*(freq*1e9-m['center_frequency'][0])*times)
            np.testing.assert_allclose(drive.pulse.samples, expected, atol=1e-12)
            self.assertTrue(any(type(inst).__name__=='Acquire' for _,inst in instructions))
        result=m['spec01_job'].result()
        self.assertTrue(result.success)
        self.assertEqual(len(result.results),71)
        for experiment in result.results:
            self.assertTrue(experiment.success)
            self.assertEqual(experiment.shots,512)
        for i in range(71):
            self.assertTrue(np.isfinite(np.asarray(result.get_memory(i))).all())

if __name__ == "__main__":
    unittest.main()
