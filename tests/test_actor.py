import pytest
from domainmodel.actor import Actor


@pytest.fixture
def actor():
    return Actor("Firstname Lastname")


def test_constructor():
    actor = Actor("123")
    assert actor.actor_full_name == "123"


def test_constructor_with_empty_string_actor_full_name():
    actor = Actor("")
    assert actor.actor_full_name is None


def test_constructor_with_non_string_actor_full_name():
    actor = Actor(42)
    assert actor.actor_full_name is None


def test_constructor_strips_whitespace():
    actor = Actor("        Firstname Lastname      ")
    assert actor.actor_full_name == "Firstname Lastname"


def test_repr(actor):
    assert repr(actor) == "<Actor Firstname Lastname>"


def test_repr_with_no_name():
    actor = Actor("")
    assert repr(actor) == "<Actor None>"


def test_equality_when_equal(actor):
    other = Actor("Firstname Lastname")
    assert actor == other


def test_equality_when_not_equal(actor):
    other = Actor("ActorName2")
    assert actor != other


def test_equality_with_different_type(actor):
    assert actor != 123


def test_less_than_when_true(actor):
    a = Actor("a")
    b = Actor("b")
    assert a < b


def test_less_than_when_false(actor):
    a = Actor("a")
    b = Actor("b")
    assert not (b < a)


def test_less_than_with_different_type(actor):
    with pytest.raises(TypeError):
        _ = actor < 123


def test_hash(actor):
    assert hash(actor) == hash(actor)


def test_hash_changes(actor):
    other = Actor("123")
    assert hash(actor) != hash(other)


def test_add_colleague(actor):
    colleague = Actor('b')
    actor.add_actor_colleague(colleague)
    assert colleague in actor.colleagues


def test_add_colleague_with_invalid_type(actor):
    with pytest.raises(TypeError):
        actor.add_actor_colleague(123)


def test_add_duplicate_colleague(actor):
    colleague = Actor('b')
    actor.add_actor_colleague(colleague)
    actor.add_actor_colleague(colleague)
    assert len(actor.colleagues) == 1


def test_check_if_this_actor_worked_with_when_true(actor):
    colleague = Actor('b')
    actor.add_actor_colleague(colleague)
    assert actor.check_if_this_actor_worked_with(colleague)


def test_check_if_this_actor_worked_with_when_false(actor):
    colleague_a = Actor('A')
    colleague_b = Actor('b')
    actor.add_actor_colleague(colleague_a)
    assert not actor.check_if_this_actor_worked_with(colleague_b)


def test_check_if_this_actor_worked_with_with_invalid_type(actor):
    with pytest.raises(TypeError):
        actor.check_if_this_actor_worked_with(123)
