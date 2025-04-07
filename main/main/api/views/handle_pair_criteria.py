import json
import numpy as np
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..database import SessionLocal
from ..models.pair_of_criterias import Pair_Of_Criterias
from ..models.caculators import Caculators


def handle_rank(matrix):
    ranks = np.argsort(-matrix)
    ranking = np.empty_like(ranks)
    ranking[ranks] = np.arange(1, len(matrix) + 1)
    combine_array = np.column_stack((matrix, ranking))
    return combine_array


@api_view(["POST"])
def handle_point_criteria(request):
    try:
        matrix_get = request.data.get("matrix")
        caculatorId = request.data.get("caculatorId")
        session = SessionLocal()
        caculator = session.query(Caculators).filter(Caculators.id == caculatorId).first()
        if caculator:
            matrix = np.array(matrix_get, dtype=float)
            rows, cols = matrix.shape
            n = rows - 1
            sum_row = matrix[rows - 1]
            matrix = np.delete(matrix, rows - 1, axis=0)
            normalised_matrix = matrix / sum_row
            weighting_matrix = np.mean(normalised_matrix, axis=1)
            consistency_rate_matrix = matrix * weighting_matrix
            weighted_sum = np.sum(consistency_rate_matrix, axis=1)
            consistency_vector = weighted_sum / weighting_matrix
            lamda_max = np.mean(consistency_vector)
            CI = (lamda_max - n)/(n - 1)
            RI_dict = {1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}
            RI = RI_dict.get(n, 1.49)
            CR = CI/RI
            matrix1 = np.column_stack((normalised_matrix, weighting_matrix))
            matrix2_1 = np.column_stack((consistency_rate_matrix, weighted_sum))
            matrix2_2 = np.column_stack((matrix2_1, consistency_vector))
            matrix_to_json = json.dumps(matrix.tolist())
            new_criteria = Pair_Of_Criterias(caculatorId=caculatorId, matrix=matrix_to_json, cr=CR)
            rank_criteria = handle_rank(weighting_matrix)
            session.add(new_criteria)
            session.commit()
            session.close()
            return Response({
                "status": "Success",
                "matrix1": matrix1.tolist(),
                "matrix2": matrix2_2.tolist(),
                "rank": rank_criteria,
                "lamda max": lamda_max,
                "CI": CI,
                "RI": RI,
                "CR": CR
            })
        else:
            session.close()
            return Response({"status": "Not Found", "message": "Mã bài tính không tồn tại!"})
    except Exception as ex:
        return Response({
            "status": "Server Error",
            "error": str(ex)
        })


@api_view(["GET"])
def get_criterias(request):
    try:
        caculatorId = request.GET.get("caculatorId")
        session = SessionLocal()
        caculator = session.query(Caculators).filter(Caculators.id == caculatorId).first()
        if caculator:
            matrix_criteria = session.query(Pair_Of_Criterias).filter(Pair_Of_Criterias.caculatorId == caculatorId).first()
            if matrix_criteria:
                matrix = json.loads(matrix_criteria.matrix)
                session.close()
                return Response({
                    "status": "Success",
                    "matrix": matrix,
                    "CR": matrix_criteria.cr
                })
            else:
                session.close()
                return Response({"status": "Success", "matrix": [], "CR": 0})
        else:
            session.close()
            return Response({"status": "Not Found", "message": "Mã bài tính không tồn tại!"})
    except Exception as ex:
        return Response({
            "status": "Server Error",
            "error": str(ex)
        })