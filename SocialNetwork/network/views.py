# Create your views here.
import datetime
import random
import operator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from users.models import Profile, User,Follow,Notification
from network.forms import UserProfileForm
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from network.models import Post,Film,PostComment,Like
from django.shortcuts import render


@login_required()
def user_profile(request , username , change = ""):
    me = request.user #logined user.
    me_profile = Profile.objects.get(user = me)
    profiles = Profile.objects.all()
    films = Film.objects.all()
    notif = Notification.objects.filter(user = me)
    if notif.__len__() > 4:
        notif = notif[notif.__len__()-4:notif.__len__()]

    cfilm= []
    if films.__len__()<3:
        cfilm = films
    else:
        i1= random.randint(0,films.__len__()-1)
        i2= random.randint(0,films.__len__()-1)
        while i1==i2:
            i2= random.randint(0,films.__len__()-1)
        cfilm[0]= films[i1]
        cfilm[1]= films[i2]
    cprof= []
    if profiles.__len__()<10:
        for prof in profiles:
            if prof != me_profile:
                cprof += [prof,]
    # else:
    #     i1= random.randint(0,profiles.__len__()-1)
    #     i2= random.randint(0,profiles.__len__()-1)
    #     while i1==i2:
    #         i2= random.randint(0,profiles.__len__()-1)
    #     cprof[0]= profiles[i1]
    #     cprof[1]= profiles[i2]
    user = User.objects.get(username = username)
    profile = Profile.objects.get(user = user)
    posts = Post.objects.filter(author = profile)
    followed = Follow.objects.filter(follower = profile)
    followedBy = Follow.objects.filter(followed = profile)

    if me != user:
        if request.method == 'GET':
            status = 'unfollow'
            changestatus = Follow.objects.filter(follower = me_profile , followed = profile)
            if changestatus:
                status = 'follow'

            if change == 'followchange':
                #add user to followed of me
                #change the statuse of follow
                if status == 'unfollow':
                    Follow.objects.create(follower = me_profile , followed = profile)
                    #notification set;
                    Notification.objects.create(producer = me.profile , user = user ,
                                                content = '{} followed {}.'.format(me.profile , user))
                    status = 'follow'

                else:
                #remove user from followed of me
                #change the statuse of follow
                    Follow.objects.get(follower = me_profile , followed = profile).delete()
                    Notification.objects.create(producer = me.profile , user = user ,
                                                content = '{} unfollowed {}.'.format(me.profile , user))
                    status = 'unfollow'
                return redirect('/profile/{}/'.format(username))

            returned_list = {'user' : user , 'userprofile' : profile , 'me': me , 'posts':posts , 'cprof':cprof,'cfilm':cfilm,
                       'followed':followed.__len__() , 'followedBy': followedBy.__len__() , 'status':status, 'notifs':notif}
            return render(request , 'userprofile.html',returned_list ,)
    else:#me == user
        if request.method == 'GET':
            if change == 'edit':
                status = 'edit'
                form = UserProfileForm()
                returned_list = {'user' : user , 'userprofile' : profile , 'me': me , 'posts':posts ,'cprof':cprof,'cfilm':cfilm,
                       'followed':followed.__len__() , 'followedBy': followedBy.__len__() , 'status':status , 'form':form , 'notifs':notif}
                return render(request, 'userprofile.html' , returned_list)

            returned_list = {'user' : user , 'userprofile' : profile , 'me': me , 'posts':posts ,'cprof':cprof,'cfilm':cfilm,
                'followed':followed.__len__() , 'followedBy': followedBy.__len__() , 'notifs':notif}
            return render(request , 'userprofile.html',returned_list,)

        elif request.method == 'POST':
            form = UserProfileForm(request.POST, instance=profile)
            if form.is_valid():
                form.save()
            # else:
                #error messages show


            return redirect('/profile/{}/'.format(username))



@login_required()
def timeline(request,username):
    me = request.user #logined user.
    me_profile = Profile.objects.get(user = me)
    profiles = Profile.objects.all()
    films = Film.objects.all()
    notif = Notification.objects.filter(user = me)
    if notif.__len__() > 4:
        notif = notif[notif.__len__()-4:notif.__len__()]
    cfilm= []
    if films.__len__()<3:
        cfilm = films
    else:
        i1= random.randint(0,films.__len__()-1)
        i2= random.randint(0,films.__len__()-1)
        while i1==i2:
            i2= random.randint(0,films.__len__()-1)
        cfilm[0]= films[i1]
        cfilm[1]= films[i2]
    cprof= []
    if profiles.__len__()<10:
        for prof in profiles:
            if prof != me_profile:
                cprof += [prof,]
    # else:
        # i1= random.randint(0,profiles.__len__()-1)
        # i2= random.randint(0,profiles.__len__()-1)
        # while i1==i2:
        #     i2= random.randint(0,profiles.__len__()-1)
        # cprof[0]= profiles[i1]
        # cprof[1]= profiles[i2]
    user = User.objects.get(username = username)
    profile = Profile.objects.get(user = user)
    followed = Follow.objects.filter(follower = profile)

    er = ''
    if me != user:
        return HttpResponseRedirect("/profile/{}".format(username))
    posts =[]
    for follower in followed:
        posts += Post.objects.filter(author = follower.followed)

    posts= sorted(posts,key= operator.attrgetter('pub_date'), reverse=True)
    c = []
    for post in posts:
        c1 = PostComment.objects.filter(post = post).order_by('-timestamp')
        c += [c1, ]
    liked1 = Like.objects.filter(liker = me)
    liked = []
    for like1 in liked1:
        liked += [like1.post,]
    if posts.__len__() == 0 :
       er = 'no post yet'
    returned_list = {'posts': posts ,'c': c ,'me': me, 'pme': me_profile, 'time': datetime.datetime.now, 'er': er, 'cprof':cprof,'cfilm':cfilm,'notifs':notif}
    return render(request , 'timeline.html',returned_list,)


@login_required()
def onepost(request,username,post_id):
    me = request.user #logined user.
    me_profile = Profile.objects.get(user = me)
    notif = Notification.objects.filter(user = me)
    if notif.__len__() > 4:
        notif = notif[notif.__len__()-4:notif.__len__()]

    profiles = Profile.objects.all()
    films = Film.objects.all()
    cfilm= []
    if films.__len__()<3:
        cfilm = films
    else:
        i1= random.randint(0,films.__len__()-1)
        i2= random.randint(0,films.__len__()-1)
        while i1==i2:
            i2= random.randint(0,films.__len__()-1)
        cfilm[0]= films[i1]
        cfilm[1]= films[i2]
    cprof= []
    if profiles.__len__()<10:
        for prof in profiles:
            if prof != me_profile:
                cprof += [prof,]
    # else:
    #     i1= random.randint(0,profiles.__len__()-1)
    #     i2= random.randint(0,profiles.__len__()-1)
    #     while i1==i2:
    #         i2= random.randint(0,profiles.__len__()-1)
    #     cprof[0]= profiles[i1]
    #     cprof[1]= profiles[i2]
    user = User.objects.get(username = username)
    author = Profile.objects.get(user = user)
    p = Post.objects.filter(id = post_id)[0]

    comments = PostComment.objects.filter(post = p).order_by('-timestamp')
    liked1 = Like.objects.filter(liker = me)
    liked = []
    for like1 in liked1:
        liked += [like1.post,]
    return render(request,'post.html',{
        'post': p,
        'c':comments,
        'author':author,
        'time': datetime.datetime.now(),
        'me':me,
        'pme':me_profile,
        'likes': liked,
        'cprof':cprof,'cfilm':cfilm,
        'notifs':notif
    })

@login_required()
def film_profile(request , film_id):
    me = request.user #logined user.
    me_profile = Profile.objects.get(user = me)
    notif = Notification.objects.filter(user = me)
    if notif.__len__() > 4:
        notif = notif[notif.__len__()-4:notif.__len__()]

    profiles = Profile.objects.all()
    films = Film.objects.all()
    cfilm= []
    if films.__len__()<3:
        cfilm = films
    else:
        i1= random.randint(0,films.__len__()-1)
        i2= random.randint(0,films.__len__()-1)
        while i1==i2:
            i2= random.randint(0,films.__len__()-1)
        cfilm[0]= films[i1]
        cfilm[1]= films[i2]
    cprof= []
    if profiles.__len__()<10:
        for prof in profiles:
            if prof != me_profile:
                cprof += [prof,]
    # else:
    #     i1= random.randint(0,profiles.__len__()-1)
    #     i2= random.randint(0,profiles.__len__()-1)
    #     while i1==i2:
    #         i2= random.randint(0,profiles.__len__()-1)
    #     cprof[0]= profiles[i1]
    #     cprof[1]= profiles[i2]

    film = Film.objects.filter(id = film_id)[0]

    if request.method == 'GET':
        returned_list = {'film': film , 'me': request.user ,'cprof':cprof,'cfilm':cfilm,'notifs':notif}
        return render(request , 'filmprofile.html' , returned_list)

    else:
        #request.method == post,  post submited
        print(request.POST.get('vote_result','10'))
        film.rating = (film.total_rate * film.rating + int(request.POST.get('vote_result','10')))/(film.total_rate +1)
        film.total_rate = film.total_rate +1
        post_body = request.POST.get('post_text' , '')
        author = Profile.objects.filter(user = request.user)[0]
        if (post_body != ''):
            Post.objects.create(film = film , body = post_body , author = author )
            film.save()
        return redirect('/film/{}'.format(film_id))


@login_required()
def search(request , kind = 'film' , value = ''):
    me_profile = Profile.objects.get(user = request.user)
    profiles = Profile.objects.all()
    films = Film.objects.all()
    notif = Notification.objects.filter(user = request.user)
    if notif.__len__() > 4:
        notif = notif[notif.__len__()-4:notif.__len__()]

    cfilm= []
    if films.__len__()<3:
        cfilm = films
    else:
        i1= random.randint(0,films.__len__()-1)
        i2= random.randint(0,films.__len__()-1)
        while i1==i2:
            i2= random.randint(0,films.__len__()-1)
        cfilm[0]= films[i1]
        cfilm[1]= films[i2]
    cprof= []
    if profiles.__len__()<10:
        for prof in profiles:
            if prof != me_profile:
                cprof += [prof,]
    # else:
    #     i1= random.randint(0,profiles.__len__()-1)
    #     i2= random.randint(0,profiles.__len__()-1)
    #     while i1==i2:
    #         i2= random.randint(0,profiles.__len__()-1)
    #     cprof[0]= profiles[i1]
    #     cprof[1]= profiles[i2]
    html_file = 'filmsearch.html'
    returned_list = {'me' : request.user , 'notifs':notif}
    if request.method == 'GET':
        if value == '':
            current_value = request.GET.get('search_value','')
            return redirect('{}/'.format(current_value))
        if kind == 'film':
            film_result = Film.objects.filter(title__icontains = value)
            returned_list = {'me':request.user , 'result':film_result , 'cprof':cprof,'cfilm':cfilm,
                             'film_active':'active' , 'user_active':'', 'key':value , 'notifs':notif}
            html_file = 'filmsearch.html'

        elif kind == 'user':
            user_result = User.objects.filter(username__icontains = value)
            returned_list = {'me':request.user , 'result':user_result , 'film_active':'' ,'cprof':cprof,'cfilm':cfilm,
                             'user_active':'active','key':value , 'notifs':notif }
            html_file = 'usersearch.html'
        return render(request, html_file , returned_list)


@login_required()
def follow(request , follow , username):
    notif = Notification.objects.filter(user = request.user)
    if notif.__len__() > 4:
        notif = notif[notif.__len__()-4:notif.__len__()]

    print(username)
    user = User.objects.get(username = username)
    if follow == 'followed':
        followed = Follow.objects.filter(follower = user.profile)
        print(followed)
        returned_list = {'me': request.user , 'followed':followed , 'follower':'' , 'notifs':notif}
    elif follow == 'followedby':
        followed_by = Follow.objects.filter(followed = user.profile)
        print(followed_by)
        returned_list = {'me': request.user , 'follower':followed_by , 'followed':'' , 'notifs':notif}
    else:
        return HttpResponse(404)

    return render(request , 'users.html' , returned_list)


@login_required()
def add_comment(request):
    notif = Notification.objects.filter(user = request.user)
    if notif.__len__() > 4:
        notif = notif[notif.__len__()-4:notif.__len__()]

    username = request.GET.get('username')
    comment = request.GET.get('comment')
    time = request.GET.get('time')
    post_id = request.GET.get('postid')

    # if not (username and comment and post_id):
    #     return HttpResponse("Not enough information.", status=400)

    post = Post.objects.get(id= post_id)

    postcomment = PostComment()
    user = User.objects.get(username = username)
    postcomment.user = Profile.objects.get(user = user)
    postcomment.comment = comment
    postcomment.post = post
    postcomment.timestamp = datetime.datetime.now()
    postcomment.save()

    post.numComments += 1
    post.save()

    author_note = Notification()
    author_note.user = post.author.user
    author_note.producer = postcomment.user
    author_note.content = '{} comment on your {} post'.format(author_note.producer.user.username,post.film.title)
    author_note.save()

    postcomments = PostComment.objects.filter(post=post)

    for c in postcomments:
        if c.user.user != postcomment.user:
            u_note = Notification()
            u_note.user = c.user.user
            u_note.producer = postcomment.user
            u_note.content = '{} comment on the {} post you commented'.format(u_note.producer.user.username,post.film.title)
            u_note.save()

    return HttpResponse("s")


def like(request):
    username = request.GET.get('username')
    post_id = request.GET.get('postid')
    k = request.GET.get('k')
    post = Post.objects.get(id= post_id)
    user = User.objects.get(username = username)
    if k=='like':
        like1 = Like()
        like1.liker = user
        like1.post = post
        like1.save()

        post.numlike += 1
        post.save()

        author_note = Notification()
        author_note.user = post.author.user
        author_note.producer = user.profile
        author_note.content = '{} پست {} تو را لایک کرده است'.format(author_note.producer.user.username,post.film.title)
        author_note.save()
    else:
        like2 = Like.objects.filter(liker = user).filter(post = post)
        like2.delete()

        post.numlike -= 1
        post.save()

    return HttpResponse("s")
