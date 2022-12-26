from sqlalchemy import Column , Integer , String , Boolean ,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null , text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from app.database import Base

class Post(Base):

    __tablename__ = "postdata"

    id = Column(Integer , primary_key = True , nullable = False)
    title = Column(String , nullable = False)
    content = Column(String , nullable = False)
    published = Column(Boolean , server_default = 'TRUE' )
    rating = Column(Integer , server_default = '0')
    createdAt = Column(TIMESTAMP(timezone=True) , nullable = False , server_default = text('now()'))
    owner_id = Column(Integer,ForeignKey("userdata.id" , ondelete="CASCADE"),nullable = False)
    owner = relationship("User")

class User(Base):
    
    __tablename__ = "userdata"

    id = Column(Integer , primary_key = True , nullable= False )
    email = Column(String , nullable = False , unique= True)
    password = Column(String , nullable = False)
    createdAt = Column(TIMESTAMP(timezone=True) , nullable = False , server_default = text('now()'))

class Votes(Base):
    
    __tablename__ = "votedata"
    post_id = Column(Integer , ForeignKey("postdata.id" , ondelete="CASCADE"),nullable = False , primary_key = True)
    user_id = Column(Integer , ForeignKey("userdata.id" , ondelete="CASCADE"),nullable = False , primary_key = True)
    