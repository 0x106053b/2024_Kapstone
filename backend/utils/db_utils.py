from backend.db.session import engine, Base


async def reset_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        print("Tables successfully dropped")

        await conn.run_sync(Base.metadata.create_all)
        print("Tables successfully dropped")

# def create_tables():
#     drop_tables()
#     Base.metadata.create_all(bind=engine)
#     print("Tables successfully created")
#
# def drop_tables():
#     Base.metadata.drop_all(bind=engine)
#     print("Tables successfully dropped")