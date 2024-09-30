from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter, OpenApiTypes
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404, redirect, render


from shortener.models import Link
from link import serializers

class LinkViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs"""
    serializer_class = serializers.LinkSerializer
    queryset = Link.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve recipes for authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-id')
    
    def perform_create(self, serializer):
        """Create new link"""
        serializer.save(user=self.request.user)


def redirect_to_original(request, short_url):
    try:
        link = Link.objects.get(short_url=short_url)
        if link:
            link.times_accessed += 1
            link.save()
    except:
        return render(request, 'link_not_found.html')

    # return redirect(link.original_url)
    return redirect_interstitial(request, link.original_url)

def redirect_interstitial(request, original_url):    
    context = {
        'original_url': original_url
    }
    
    return render(request, 'redirecting.html', context)
