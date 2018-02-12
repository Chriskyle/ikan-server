from rest_framework.views import APIView

from ikan.core import paginator
from ikan.models import Solution
from ikan.serializers import SolutionSerializer


class HelpDocumentView(APIView):

    @staticmethod
    def get(request):
        solutions = Solution.objects.all()
        return paginator.api_paging(solutions, request, SolutionSerializer)
