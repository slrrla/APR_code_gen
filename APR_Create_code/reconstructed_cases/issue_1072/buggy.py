from qiskit.visualization.bloch import Bloch
from sympy.physics.matrices import msigma
from sympy import Matrix
from sympy import N, re
import numpy as np

def to_spherical(vec):
    x = np.real(vec[0])
    y = np.real(vec[1])
    z = np.real(vec[2])
    hxy = np.hypot(x, y)
    r = np.hypot(hxy, z)
    ϕ = np.arctan2(y, x)  # az
    θ = np.arctan2(z, hxy)  # el
    return [r, ϕ, θ]

def to_cartesian(polar):
    r = polar[0]
    ϕ = polar[1]
    θ = polar[2]
    x = r * np.sin(ϕ) * np.cos(θ)
    y = r * np.sin(ϕ) * np.sin(θ)
    z = r * np.cos(ϕ)
    return [np.real(x), np.real(y), np.real(z)]

def rn_su2(vec, rot_angle, n):
    spherical_vec = to_spherical(vec)
    ϕ = spherical_vec[1]
    θ = spherical_vec[2]
    sx = msigma(1)
    sy = msigma(2)
    sz = msigma(3)
    M_q = (np.sin(θ)*np.cos(ϕ)*sx + np.sin(θ)*np.sin(ϕ)*sy + np.cos(θ)*sz)
    U_n = np.eye(2)*np.cos(rot_angle/2) - 1j*(n[0]*sx+n[1]*sy+n[2]*sz)*np.sin(rot_angle/2)
    M_q_rotated = U_n*M_q*np.matrix(U_n).H
    return M_q_rotated

def extract_angles(M_q_rotated):
    cos_θ_rotated = float(N(re(M_q_rotated[0,0])))
    θ_rotated = np.arccos(cos_θ_rotated)
    # e^(ix) = cos(x) + i*sin(x)
    # see https://en.wikipedia.org/wiki/Euler%27s_identity
    temp = float(N(re(M_q_rotated[1,0])))
    temp = temp/np.sin(θ_rotated)
    ϕ_rotated = np.arccos(temp)
    return (ϕ_rotated, θ_rotated)

rot_angle = np.pi/8
n = [0, 0, 1]
start_vec = [1, 0, 0]
num_iterations = 5
_bloch = Bloch()
_bloch.vector_color = ['blue'] * num_iterations
sv = []
vec = start_vec
sv.append(vec)
for i in range(num_iterations):
    M_q_rotated = rn_su2(vec, rot_angle, n)
    (ϕ_rotated, θ_rotated) = extract_angles(M_q_rotated)
    vec = np.array(to_cartesian([1, ϕ_rotated, θ_rotated]))
    sv.append(vec)
_bloch.add_vectors(sv)
_bloch.render()
