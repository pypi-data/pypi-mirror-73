import pytest
import sqlalchemy as sa

from sqlalchemy_utils import get_mapper


class TestGetMapper(object):

    @pytest.fixture
    def Building(self, Base):
        class Building(Base):
            __tablename__ = 'building'
            id = sa.Column(sa.Integer, primary_key=True)
        return Building

    def test_table(self, Building):
        assert get_mapper(Building.__table__) == sa.inspect(Building)

    def test_declarative_class(self, Building):
        assert (
            get_mapper(Building) ==
            sa.inspect(Building)
        )

    def test_declarative_object(self, Building):
        assert (
            get_mapper(Building()) ==
            sa.inspect(Building)
        )

    def test_mapper(self, Building):
        assert (
            get_mapper(Building.__mapper__) ==
            sa.inspect(Building)
        )

    def test_class_alias(self, Building):
        assert (
            get_mapper(sa.orm.aliased(Building)) ==
            sa.inspect(Building)
        )

    def test_instrumented_attribute(self, Building):
        assert (
            get_mapper(Building.id) == sa.inspect(Building)
        )

    def test_table_alias(self, Building):
        alias = sa.orm.aliased(Building.__table__)
        assert (
            get_mapper(alias) ==
            sa.inspect(Building)
        )

    def test_column(self, Building):
        assert (
            get_mapper(Building.__table__.c.id) ==
            sa.inspect(Building)
        )

    def test_column_of_an_alias(self, Building):
        assert (
            get_mapper(sa.orm.aliased(Building.__table__).c.id) ==
            sa.inspect(Building)
        )


class TestGetMapperWithQueryEntities(object):

    @pytest.fixture
    def Building(self, Base):
        class Building(Base):
            __tablename__ = 'building'
            id = sa.Column(sa.Integer, primary_key=True)
        return Building

    @pytest.fixture
    def init_models(self, Building):
        pass

    def test_mapper_entity_with_mapper(self, session, Building):
        entity = session.query(Building.__mapper__)._entities[0]
        assert (
            get_mapper(entity) ==
            sa.inspect(Building)
        )

    def test_mapper_entity_with_class(self, session, Building):
        entity = session.query(Building)._entities[0]
        assert (
            get_mapper(entity) ==
            sa.inspect(Building)
        )

    def test_column_entity(self, session, Building):
        query = session.query(Building.id)
        assert get_mapper(query._entities[0]) == sa.inspect(Building)


class TestGetMapperWithMultipleMappersFound(object):

    @pytest.fixture
    def Building(self, Base):
        class Building(Base):
            __tablename__ = 'building'
            id = sa.Column(sa.Integer, primary_key=True)

        class BigBuilding(Building):
            pass

        return Building

    def test_table(self, Building):
        with pytest.raises(ValueError):
            get_mapper(Building.__table__)

    def test_table_alias(self, Building):
        alias = sa.orm.aliased(Building.__table__)
        with pytest.raises(ValueError):
            get_mapper(alias)


class TestGetMapperForTableWithoutMapper(object):

    @pytest.fixture
    def building(self):
        metadata = sa.MetaData()
        return sa.Table('building', metadata)

    def test_table(self, building):
        with pytest.raises(ValueError):
            get_mapper(building)

    def test_table_alias(self, building):
        alias = sa.orm.aliased(building)
        with pytest.raises(ValueError):
            get_mapper(alias)
