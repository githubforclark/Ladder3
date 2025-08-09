from django.db import models

# Create your models here.


class Blogs(models.Model):
    ID = models.AutoField(primary_key=True)
    blog_title = models.CharField(max_length=30)
    blog_describe = models.CharField(max_length=256)
    blog_imglink = models.CharField(max_length=256)
    blog_content = models.TextField()
    blog_status = models.CharField(max_length=30)
    create_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间',auto_now=True)
    class Meta:
        db_table = 'Blogs'
        def __str__(self):
            return self.blog_name
        
class Visions(models.Model):
    ID = models.AutoField(primary_key=True)
    vision_title = models.CharField(max_length=30)
    vision_describe = models.CharField(max_length=256)
    vision_imglink = models.CharField(max_length=256)
    vision_content = models.TextField()
    vision_jumbo_title = models.CharField(max_length=30)
    vision_jumbo_space = models.CharField(max_length=256)
    vision_jumbo_imglink = models.CharField(max_length=256)
    vision_status = models.CharField(max_length=30)
    create_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间',auto_now=True)
    class Meta:
        db_table = 'Visions'
        def __str__(self):
            return self.vision_title
        
class Books(models.Model):
    ID = models.AutoField(primary_key=True)
    book_title = models.CharField(max_length=30)
    book_describe = models.CharField(max_length=256)
    book_imglink = models.CharField(max_length=256)
    book_content = models.TextField()
    book_jumbo_title = models.CharField(max_length=30)
    book_jumbo_space = models.CharField(max_length=256)
    book_jumbo_imglink = models.CharField(max_length=256)
    book_status = models.CharField(max_length=30)
    create_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间',auto_now=True)
    class Meta:
        db_table = 'Books'
        def __str__(self):
            return self.book_title
        
class BlogComment(models.Model):
    ID = models.AutoField(primary_key=True)
    BlogID = models.IntegerField()
    UserName = models.CharField(max_length=30)
    CommentBody = models.TextField()
    create_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    class Meta:
        db_table = 'BlogComment'
        def __str__(self):
            return self.UserName
        
class VisionComment(models.Model):
    ID = models.AutoField(primary_key=True)
    VisionID = models.IntegerField()
    UserName = models.CharField(max_length=30)
    CommentBody = models.TextField()
    create_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    class Meta:
        db_table = 'VisionComment'
        def __str__(self):
            return self.UserName
        
class BookComment(models.Model):
    ID = models.AutoField(primary_key=True)
    BookID = models.IntegerField()
    UserName = models.CharField(max_length=30)
    CommentBody = models.TextField()
    create_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    class Meta:
        db_table = 'BookComment'
        def __str__(self):
            return self.UserName
        
class Next_People(models.Model):
    ID = models.AutoField(primary_key=True)
    MailAddr = models.EmailField()
    Name = models.CharField(max_length=30)
    Keys = models.CharField(max_length=128)
    create_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间',auto_now=True)
    class Meta:
        db_table = 'Next_People'
        def __str__(self):
            return self.Name
        
class VerifyMailRecord(models.Model):
    ID = models.AutoField(primary_key=True)
    MailAddr = models.EmailField()
    Code = models.CharField(max_length=30)
    create_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    class Meta:
        db_table = 'VerifyMailRecord'
        def __str__(self):
            return self.MailAddr
