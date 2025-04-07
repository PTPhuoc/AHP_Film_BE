from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime
import pytz
from ..database import SessionLocal
from ..models.caculators import Caculators


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


def create_id():
    vn_tz = pytz.timezone("Asia/Ho_Chi_Minh")
    vn_time = datetime.now(vn_tz)
    new_id = str(vn_time.day) + str(vn_time.month) + str(vn_time.year) + str(
        vn_time.hour + vn_time.minute + vn_time.second)
    return new_id
