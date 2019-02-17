users=User.objects.all()
user1 = users[0]
user1.profile.Analysis_Type


temp = Profile.objects.get(issue=self.request.user.profile.Issue)