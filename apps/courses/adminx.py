import xadmin

from apps.courses.models import Course,Lesson,Video,CourseResource,CourseType


class GlobalSettings(object):
    site_title = "寒芒后台管理"
    site_footer = "成都寒芒科技有限公司"
    menu_style = "accordion"

#皮肤
class BaseSettings(object):
    enable_themes = True
    use_bootswatch = True

class CourseTypeAdmin(object):
    list_display = ['type','desc']
    list_editable = ['type','desc']

class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'teacher__name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    list_editable = ["degree", "desc"]
    style_fields = {'detail':'ueditor'}


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'file', 'add_time']
    search_fields = ['course', 'name', 'file']
    list_filter = ['course', 'name', 'file', 'add_time']


xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(CourseType,CourseTypeAdmin)
#xadmin 配置
xadmin.site.register(xadmin.views.CommAdminView,GlobalSettings)
xadmin.site.register(xadmin.views.BaseAdminView,BaseSettings)