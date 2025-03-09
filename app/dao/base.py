from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.database import SessionLocal


class BaseDAO:
    model = None

    @classmethod
    async def get_all(cls, **filter_by):
        """
        Асинхронно получает и возвращает все экземпляры модели, удовлетворяющие указанному критерию.
        :param filter_by: Критерий фильтрации в виде именованных параметров
        :return: Список экземпляров модели
        """
        async with SessionLocal() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def get_one_or_none_by_id(cls, data_id: int):
        """
        Асинхронно получает и возвращает один экземпляр модели по id или None.
        :param data_id: Критерий фильтрации (идентификатор записи)
        :return: Экземпляр модели или None, если ничего не найдено
        """
        async with SessionLocal() as session:
            query = select(cls.model).filter_by(id=data_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def get_one_or_none(cls, **filter_by):
        """
        Асинхронно получает и возвращает один экземпляр модели по указанному критерию или None.
        :param filter_by: Критерий фильтрации в виде именованных параметров
        :return: Экземпляр модели или None, если ничего не найдено
        """
        async with SessionLocal() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def add(cls, **data):
        """
        Асинхронно добавляет новую запись в БД.
        :param data: Данные для добавления
        :return: Экземпляр добавленной записи
        """
        async with SessionLocal() as session:
            async with session.begin():
                new_record = cls.model(**data)
                session.add(new_record)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return new_record
