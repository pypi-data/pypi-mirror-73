import pyostracker


def test_update():
    before = pyostracker.scores("zezima")
    pyostracker.update("zezima")
    after = pyostracker.scores("zezima")

    assert before["current_at"] < after["current_at"], "update() did not find hiscores"


def test_scores():
    scores = pyostracker.scores("zezima")
    assert scores["hiscores"], "scores() did not find hiscores"
