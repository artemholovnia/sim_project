from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse, Http404
from django.views.generic import TemplateView
from .forms import CreateXMLForm
from .models import *
import os
from sim.settings import MEDIA_ROOT, CONFIGURATION_TEMPLATES, CONFIGURATION_FILES
from permission.check_permission import Permission as UserPermissionCheck
from user_auth.models import UserProfile
from user_auth.views import MainInfo
import json
from sim.unique_identificator import create_identificator
from .forms import CreateXMLForm
from .models import XML
from user_auth.models import UserProfile

def file_name_validator(file_name):
    form = CreateXMLForm({'file_name':file_name})
    if form.is_valid():
        return True
    else:
        errors_list = []
        for error in form.errors:
            one_field_error_dict = {'field_name': error, 'errors': form.errors.get(error)}
            errors_list.append(one_field_error_dict)
        return errors_list

def passed_folders(path):
    path = path.split('/')
    dirs = []
    for dir in path:
        if dir == '':
            path.remove(dir)
    for index, div in enumerate(path):
        dir_dict = {'dir_name': div}
        dir_dict.update({'path': '/' + '/'.join(path[:index + 1])})
        dirs.append(dir_dict)
    return dirs

# Create your views here.
class XMLMainInfo(MainInfo):
    template_name = 'main_template.html'

    def get_context_data(self, **kwargs):
        context = super(XMLMainInfo, self).get_context_data(**kwargs)
        context['createXML_permission'] = UserPermissionCheck(self.request, 'xml', tag='C').__call__()
        context['updateXML_permission'] = UserPermissionCheck(self.request, 'xml', tag='U').__call__()
        context['deleteXML_permission'] = UserPermissionCheck(self.request, 'xml', tag='D').__call__()
        context['viewXML_permission'] = UserPermissionCheck(self.request, 'xml', tag='V').__call__()
        return context

class CreateXML(XMLMainInfo):
    from sim.settings import XML_EDITOR_DIR
    template_name = 'xml_editor/edit.html'
    xml_editor_dir = XML_EDITOR_DIR
    model_name = 'xml'

    def get_context_data(self, **kwargs):
        context = super(CreateXML, self).get_context_data(**kwargs)
        context['createXMLForm'] = CreateXMLForm
        context['existedFiles'] = XML.objects.all()
        return context

    def get(self, *args, **kwargs):
        if UserPermissionCheck(self.request, self.model_name).__call__():
            return super(CreateXML, self).get(*args, **kwargs)
        else:
            return HttpResponse('permission denied')

    def post(self, *args, **kwargs):
        if self.request.is_ajax():
            request_dict = self.request.POST
            context = super(CreateXML, self).get_context_data(**kwargs)

            #rewrite file
            if context.get('createXML_permission') is True or context.get('updateXML_permission') is True or context.get('viewXML_permission'):
                if request_dict.get('rewrite_file') is not None:
                    if context.get('createXML_permission') is True or context.get('updateXML_permission'): #проверка доступа к созданию файлов
                        request_dict = self.request.POST
                        path, content = os.path.abspath(request_dict.get('path')), request_dict.get('content')
                        with open(path, 'w', encoding='UTF-8') as conf_file:
                            conf_file.write(content)
                            conf_file.close()
                        return JsonResponse({'success':True, 'message':'updated'})
                    else:
                        return JsonResponse({'success':False, 'permission_denied':True})

            #create file
                if request_dict.get('create_file') is not None:
                    if context.get('createXML_permission') is True or context.get('updateXML_permission'): #проверка доступа к созданию файлов
                        request_dict = self.request.POST
                        file_name_valid = file_name_validator(request_dict.get('file_name'))
                        if file_name_valid == True:
                            path = self.xml_editor_dir
                            if request_dict.get('path') is not None:
                                path = os.path.abspath(request_dict.get('path'))
                            file_name, content, format = request_dict.get('file_name'), request_dict.get('content'), request_dict.get('format')
                            file_path = os.path.abspath(os.path.join(path, '.'.join([file_name, format])))
                            if os.path.exists(file_path):
                                return JsonResponse({'success': False, 'message': 'Juz istnieje, spruboj inna nazwe'})
                            else:
                                try:
                                   XML.objects.get(file_name=file_name, type=format, file=file_path)
                                except XML.DoesNotExist:
                                    with open(file_path, 'w', encoding='UTF-8') as conf_file:
                                        conf_file.write(content)
                                        conf_file.close()
                                    XML.objects.create(user=self.request.user, user_profile=UserProfile.objects.get(user=self.request.user), file_name=file_name, type=format, file=file_path)
                                    return JsonResponse({'success': True, 'message': 'created', 'file_name':'.'.join([file_name, format]), 'file_path':file_path})
                        else:
                            return JsonResponse({'success':False, 'errors':file_name_valid})
                    else:
                        return JsonResponse({'success':False, 'permission_denied':True})

                #open file
                if request_dict.get('open_file') is not None:
                    if context.get('updateXML_permission') is True or context.get('viewXML_permission') is True or context.get('createXML_permission'): #проверка на право доступа к открытию и обновлению файла
                        unique_identificator = create_identificator(8)
                        file = open(os.path.join(MEDIA_ROOT, 'configuration_files/' + unique_identificator + '.xml'), 'wb')
                        file.write(self.request.FILES['file'].read())
                        file.close()
                        file = open(os.path.join(MEDIA_ROOT, 'configuration_files/' + unique_identificator + '.xml'), 'r', encoding='UTF-8')
                        content = file.read()
                        file.close()
                        return JsonResponse({'success':True, 'content':content})
                    else:
                        return JsonResponse({'success': False, 'permission_denied': True})

                #load directory
                if request_dict.get('load_directory') is not None:
                    if context.get('updateXML_permission') is True or context.get('createXML_permission') is True: #проверка на право показа директорий для сохранения
                        start_path = os.path.realpath(os.path.dirname('manage.py'))
                        if request_dict.get('start_path') is not None:
                            start_path = request_dict.get('start_path')
                        if os.access(start_path, os.R_OK):
                            pass
                        else:
                            return JsonResponse({'success':True, 'message':'permission_denied'})
                        dirs_list = os.listdir(start_path)
                        dirs = []
                        for element in dirs_list:
                            one_element_dict = {'title':element}
                            if os.path.isfile(os.path.join(start_path, element)):
                                one_element_dict.update({'isfile':True, 'isfolder':False, 'path':os.path.abspath(os.path.join(start_path, element))})
                            if os.path.isdir(os.path.join(start_path, element)):
                                one_element_dict.update({'isfolder':True, 'isfile':False, 'path':os.path.abspath(os.path.join(start_path, element))})
                            dirs.append(one_element_dict)
                        return JsonResponse({'success':True, 'dirs':dirs, 'start_path':start_path, 'passed_dirs':passed_folders(start_path)})
                    else:
                        return JsonResponse({'success': False, 'permission_denied': True})
            else:
                return JsonResponse({'success': False, 'permission_denied': True})
        else:
            return HttpResponse('bad request')

def show_document(request, path):
    print(os.path.abspath(path))
    if os.path.exists(os.path.abspath(path)):
        response = HttpResponse(open(os.path.abspath(path), 'r', encoding='UTF-8').read())
        response['Content-Type'] = 'application/xml; charset=utf-8'
        response['file_path'] = os.path.abspath(path)
        return response
    else:
        raise Http404('file does not exist')

def delete_xml_model(request, file_id):
    if request.method == "GET":
        XML.objects.get(id=file_id).delete()
        #'HTTP_HOST': '127.0.0.1:8000'
        #'HTTP_REFERER': 'http://127.0.0.1:8000/xml_editor/edit/'
        return redirect('/' + '/'.join(request.META.get('HTTP_REFERER').split('//')[1].split('/')[1:]))
    else:
        return HttpResponse('bad request')


