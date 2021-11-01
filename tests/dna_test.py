from pytest import approx
from src.dna import DNA

dna = DNA(0, 0, 0, 1)

def test_has_constants():
    assert hasattr(dna, 'MAX_SPEED'), "DNA does not have constant: MAX_SPEED"
    assert hasattr(dna, 'MAX_TARGETING_CHANCE'), "DNA does not have constant: MAX_TARGETING_CHANCE"
    assert hasattr(dna, 'MAX_VIEW_DISTANCE'), "DNA does not have constant: MAX_VIEW_DISTANCE"
    assert hasattr(dna, 'EVOLUTION_DIFFICULTY'), "DNA does not have constant: EVOLUTION_DIFFICULTY"

def test_has_attr():
    assert hasattr(dna, 'speed'), "DNA does not have attr: speed"
    assert hasattr(dna, '_target'), "DNA does not have attr: _target"
    assert hasattr(dna, '_vision'), "DNA does not have attr: _vision"
    assert hasattr(dna, 'target'), "DNA does not have attr: target"
    assert hasattr(dna, 'vision'), "DNA does not have attr: vision"

def test_rndm_val_gen_algo():
    assert sum([DNA.rndm_num_gen(0, 5, 1, 0) for _ in range(10_000)])/10_000 == approx(2.5, abs=5e-1), "normal number generation failed"
    assert sum([DNA.rndm_num_gen(1, 5, 1, 100) for _ in range(10_000)])/10_000 == approx(1, abs=1e-1), "high convergence at curerent minimum failed"
    assert sum([max([DNA.rndm_num_gen(1, 100, 100, 1) for _ in range(10_000)]) for _ in range (5)])/5 == approx(22, abs=4), "high convergence as value gets further for minimum failed"