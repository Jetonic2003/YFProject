from dbCon import DB_URI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(DB_URI, echo=True)
Session = sessionmaker(bind=engine)
session = Session()


class TagService:
    # 添加标签
    def add_tag(self, name, description=''):
        tag = session.query(Tag).filter_by(name=name).first()
        if tag:
            return tag
        else:
            tag = Tag(name=name, description=description)
            session.add(tag)
            session.commit()
            return tag

    # 删除标签
    def remove_tag(self, id):
        tag = session.query(Tag).filter_by(id=id).first()
        if tag:
            session.delete(tag)
            session.commit()
        return tag

    # 根据 ID 获取标签信息
    def get_tag_by_id(self, id):
        tag = session.query(Tag).filter_by(id=id).first()
        return tag

    # 根据名称获取标签信息
    def get_tag_by_name(self, name):
        tag = session.query(Tag).filter_by(name=name).first()
        return tag

    # 更新标签信息
    def update_tag(self, id, name=None, description=None):
        tag = self.get_tag_by_id(id)
        if tag:
            if name:
                tag.name = name
            if description:
                tag.description = description
            session.commit()
        return tag
