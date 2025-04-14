from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime
import pytz
from ..database import SessionLocal
from ..models.caculators import Caculators
from ..models.pair_of_criterias import Pair_Of_Criterias
from ..models.criterias import Criterias
from ..models.plans import Plans


@api_view(["GET"])
def get_caculator(request):
    try:
        id = request.GET.get('id', 'No Id')
        session = SessionLocal()
        caculator = session.query(Caculators).filter(Caculators.id == id).first()
        if caculator:
            session.close()
            return Response({"caculator": {"id": caculator.id,
                                           "dateCreate": caculator.dateCreate.strftime("%d/%m/%Y %H:%M")},
                             "status": "Success"})
        else:
            new_id = create_id()
            vn_tz = pytz.timezone("Asia/Ho_Chi_Minh")
            vn_time = datetime.now(vn_tz)
            new_caculator = Caculators(id=new_id, dateCreate=vn_time)
            session.add(new_caculator)
            session.commit()
            session.close()
            return Response(
                {"caculator":
                     {"id": new_id, "dateCreate": vn_time.strftime("%d/%m/%Y %H:%M")}, 'status': "Success"})
    except Exception as ex:
        return Response({"status": "Server Error", "Error": str(ex)})


@api_view(["GET"])
def get_history(request):
    session = SessionLocal()
    try:
        all_caculator = session.query(Caculators).all()
        list_history = []
        for caculator in all_caculator:
            if session.query(Pair_Of_Criterias).filter_by(caculatorId=caculator.id).first():
                num_criteria = session.query(Criterias).filter_by(caculatorId=caculator.id).count()
                num_plan = session.query(Plans).filter_by(caculatorId=caculator.id).count()
                list_history.append({
                    "id": caculator.id,
                    "dateCreate": caculator.dateCreate,
                    "numCriteria": num_criteria,
                    "numPlan": num_plan
                })
        return Response({"status": "Success", "history": list_history})
    except Exception as ex:
        return Response({"status": "Server Error", "Error": str(ex)})
    finally:
        session.close()


def create_id():
    vn_tz = pytz.timezone("Asia/Ho_Chi_Minh")
    vn_time = datetime.now(vn_tz)
    new_id = str(vn_time.day) + str(vn_time.month) + str(vn_time.year) + str(
        vn_time.hour + vn_time.minute + vn_time.second)
    return new_id
