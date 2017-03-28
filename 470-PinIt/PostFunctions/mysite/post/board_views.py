from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from django.core.urlresolvers import reverse_lazy
from .models import User, Board, Post

def TopFiveBoard(request):
    return {'top_five_board_list': Board.objects.order_by('subscribers')[:5]}

class BoardIndexView(generic.ListView):
    template_name = 'boards/board_index.html'
    context_object_name = 'full_board_list'

    def get_queryset(self):
        return Board.objects.all()

class BoardCreate(CreateView):
    model = Board
    template_name = 'boards/board_add.html'
    fields = '__all__'

class BoardUpdate(UpdateView):
    model = Board
    template_name = 'boards/board_edit.html'
    fields = '__all__'

class BoardDetail(DetailView):
    model = Board
    template_name = 'boards/board_detail.html'

    def posts(self):
        return Post.objects.filter(board=self.kwargs['pk'])

class BoardDelete(DeleteView):
    model = Board
    success = reverse_lazy('full_board_list')

def index(request):
    full_board_list = Board.objects.all()
    context = {'full_board_list': full_board_list}
    return render(request, 'boards/board_index.html', context)


