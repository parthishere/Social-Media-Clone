from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse, reverse_lazy


@api_view(['GET',])
def api_root(requets):
    ''' All The neseccery Enddpoints will be on home page,, dynamic endpoints will be  not here! '''
    return Response({
        'data': None
    })