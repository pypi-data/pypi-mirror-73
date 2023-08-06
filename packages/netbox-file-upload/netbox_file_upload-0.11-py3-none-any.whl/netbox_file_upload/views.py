from django.shortcuts import get_object_or_404, render
from django.views.generic import View
from django.contrib.auth.mixins import PermissionRequiredMixin
from utilities.views import ObjectListView
from django.contrib import messages
import csv, io


from dcim.models import Device, DeviceType, DeviceRole, Site
from .forms import UploadFileForm


class DeviceListView(View):
    def get(self, request):
        devices = Device.objects.all()
        device1 = Device.objects.get(serial=123456789)
        device1.name = 'test2dev'
        device1.save()
        device2 = Device(name='test3', serial='12345', device_type=DeviceType.objects.get(model='test_model'), device_role=DeviceRole.objects.get(name='test_role'), site=Site.objects.get(name='test_site'), status='Active')
        device2.save()
        return render(request, 'netbox_file_upload/device_list.html', {
            'devices': devices,
            'device1': device1,
            'device2': device2,
        })

class DeviceUpload(View):
    template = 'file.html'
    prompt = 'Please upload your CSV here'

    def get(self, request):
        return render(request, 'netbox_file_upload/file.html', None)

    def post(self, request):
        csv_file = request.FILES['file']
        
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'This is not a CSV file')
            return render(request, 'netbox_file_upload/file.html', None)
        
        else:
            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            next(io_string)
            for column in csv.reader(io_string, delimiter=',', quotechar='|'):
                name = column[0]
                serial = column[1]
                device_type = DeviceType.objects.get(model=column[2])
                device_role = DeviceRole.objects.get(name=column[3])
                site = Site.objects.get(name=column[4])
                status = column[5]

                try:
                    device = Device.objects.get(serial=column[1])
                    device.name = column[0]
                    device.device_type = DeviceType.objects.get(model=column[2])
                    device.device_role = DeviceRole.objects.get(name=column[3])
                    device.site = Site.objects.get(name=column[4])
                    device.status = column[5]
                    device.save()
                except Device.DoesNotExist:
                    device = Device(
                        name = column[0],
                        serial = column[1],
                        device_type = DeviceType.objects.get(model=column[2]),
                        device_role = DeviceRole.objects.get(name=column[3]),
                        site = Site.objects.get(name=column[4]),
                        status = column[5]
                    )
                    device.save()

            messages.success(request, 'File successfully uploaded')
            return render(request, 'netbox_file_upload/file.html', None)
             

        

