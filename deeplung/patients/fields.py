from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from multiupload.fields import MultiImageField
from django import forms
#import random
#import string
from PIL import Image
import pdb
import shortuuid
import six
import sys



#def rand_slug(n):
#    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(n))


class OrderField(models.PositiveIntegerField):
    def __init__(self, for_fields=None, *args, **kwargs):
        self.for_fields = for_fields
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if getattr(model_instance, self.attname) is None:
            # no current value
            try:
                qs = self.model.objects.all()
                if self.for_fields:
                    # filter by objects with the same field values
                    # for the fields in "for_fields"
                    query = {field: getattr(model_instance, field)\
                    for field in self.for_fields}
                    qs = qs.filter(**query)
                # get the order of the last item
                last_item = qs.latest(self.attname)
                value = last_item.order + 1
            except ObjectDoesNotExist:
                value = 0
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super().pre_save(model_instance, add)


class ShortUUIDField(models.CharField):
    """
    A field which stores a Short UUID value in base57 format. This may also have
    the Boolean attribute 'auto' which will set the value on initial save to a
    new UUID value (calculated using shortuuid's default (uuid4)). Note that while all
    UUIDs are expected to be unique we enforce this with a DB constraint.
    """

    def __init__(self, auto=True, *args, **kwargs):
        self.auto = auto
        self.max_length = kwargs['max_length']
        # We store UUIDs in base57 format, which is fixed at 22 characters.
        #kwargs['max_length'] = 22
        if auto:
            # Do not let the user edit UUIDs if they are auto-assigned.
            kwargs['editable'] = False
            kwargs['blank'] = True
            kwargs['unique'] = True  # if you want to be paranoid, set unique=True in your instantiation of the field.

        super(ShortUUIDField, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        """
        This is used to ensure that we auto-set values if required.
        See CharField.pre_save
        """
        value = super(ShortUUIDField, self).pre_save(model_instance, add)
        if self.auto and not value:
            # Assign a new value for this attribute if required.
            value = six.text_type(shortuuid.ShortUUID().random(length=self.max_length))
            setattr(model_instance, self.attname, value)
        return value

    def formfield(self, **kwargs):
        if self.auto:
            return None
        return super(ShortUUIDField, self).formfield(**kwargs)

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], [r"^shortuuidfield\.fields\.ShortUUIDField"])
except ImportError:
    pass
    
    
#class SlicesField(models.ImageField):
#    def __init__(self, ct=None, upload_to='images', *args, **kwargs):
#        self.ct = ct
#        #pdb.set_trace()
#        super().__init__(null=True, blank=True, upload_to='images', *args, **kwargs)
#    
#    def get_slices(self):
#        pdb.set_trace()
#        if hasattr(obj, 'ct'):
#            idxs = [i+1 for i in range(len(obj.ct.path)) if obj.ct.path[i]=='/']
#            name = './tmp/' + obj.ct.path[idxs[-1]:]
#            with open(name, 'wb') as f:
#                f.write(obj.ct.read())
#                
#            img = nib.load(name)
#            #pdb.set_trace()
#            #print(img.get_fdata().shape)
#            images = [Image.fromarray(np.array(img.get_fdata()[:,:,i])) for i in range(img.get_fdata().shape[2])]
#            os.remove(name)
#            #plt.imshow(img.get_fdata()[:,:,int(img.shape[2]/2)])
#            
#            #dicom = dcmread(self.ct)
#            #tensor = np.array(dicom.pixel_array)
#        
#            #images = MultiImageField(min_num=1, max_num=300, max_file_size=None)
#            #pdb.set_trace()
#        
#            # save single slices
#            return images
#    
#    def pre_save(self, model_instance, add):
#        pdb.set_trace()
#        file = self.get_slices()
#        if file and not file._committed:
#            # Commit the file to storage prior to saving the model
#            file.save(file.name, file.file, save=False)
#        return file
#    
#    def save(self, name, content, save=True):
#        pdb.set_trace()
#        content = self.get_slices()
#        name = self.field.generate_filename(self.instance, name)
#        self.name = self.storage.save(name, content, max_length=self.field.max_length)
#        super().save(name, content, *args, **kwargs)
    
    
