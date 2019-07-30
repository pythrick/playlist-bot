from utils import normalizer


def test_normalize_string():
    comment = 'Il posto + freddo @me.renda_'
    result = normalizer.normalize_string(comment)
    assert result == 'Il Posto + Freddo'


def test_same_title():
    art1 = 'Guns and Roses'
    art2 = 'Guns + Roses'
    result = normalizer.same_title(art1, art2)
    assert result is True


def test_same_title_equal_name():
    art1 = 'Guns and Roses'
    art2 = 'Guns AND Roses'
    result = normalizer.same_title(art1, art2)
    assert result is True


def test_same_title_one_contains_another():
    art1 = 'Guns and Roses'
    art2 = 'November Rain - Guns AND Roses'
    result = normalizer.same_title(art1, art2)
    assert result is True


def test_same_title_one_contains_another_2():
    art1 = 'November Rain - Guns AND Roses'
    art2 = 'Guns and Roses'
    result = normalizer.same_title(art1, art2)
    assert result is True


def test_same_title_close_by_similarity():
    art1 = 'Phantom of Ophera'
    art2 = 'phanton of opera'
    result = normalizer.same_title(art1, art2)
    assert result is True


def test_different_titles():
    art1 = 'Metallica'
    art2 = 'Guns and Roses'
    result = normalizer.same_title(art1, art2)
    assert result is False


def test_normalizer_comments():
    comments = [
        "Ricky Manning - LA Is Lonely",
        "@b.marijamagdalena DA!",
        "The less I know the better- Tame impala",
        "Ojo Sujono @didikempot_official 😥😥",
        "\"Somewhere i belong\" - Linkin Park and \"Lovely\" - Billie Eilish & Kahled",
        "The house of wolves - Bring me the horizon",
        "Lay me down -Sam Smith",
        "YouTube Rewind 2018 😌👌🏼",
        "Martin Garrix- So Far Away",
        "Mine - bazzi",
        "Don McLean - Vincent (Starry, Starry Night)",
        "Thierry [Coolest guy]",
        "mc Mirella",
        "super boy band",
        "Metropolitam orchestra",
    ]
    result = [normalizer.normalize_string(x) for x in comments]
    assert result[0] == "Ricky Manning - La Is Lonely"
    assert result[1] == ""
    assert result[2] == "The Less I Know The Better - Tame Impala"
    assert result[3] == "Ojo Sujono"
    assert result[4] == ""
    assert result[5] == "The House Of Wolves - Bring Me The Horizon"
    assert result[6] == "Lay Me Down - Sam Smith"
    assert result[7] == "Youtube Rewind 2018"
    assert result[8] == "Martin Garrix - So Far Away"
    assert result[9] == "Mine - Bazzi"
    assert result[10] == "Don Mclean - Vincent"
    assert result[11] == "Thierry"
    assert result[12] == "Mirella"
    assert result[13] == "Super Boy"
    assert result[14] == "Metropolitam"


