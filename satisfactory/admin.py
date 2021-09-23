from django.contrib import admin
from .models import *

class RecipeInputInline(admin.TabularInline):
    model = RecipeInput
    extra = 1

class RecipeOutputInline(admin.TabularInline):
    model = RecipeOutput
    extra = 1

class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeInputInline, RecipeOutputInline)
    exclude = ('key',)

class FactoryRecipeInline(admin.TabularInline):
    model = FactoryRecipeAmount
    extra = 1
    fk_name = "recipe_to"

class FactoryNodeInline(admin.TabularInline):
    model = FactoryNodeAmount
    extra = 1

class FactoryRecipeAdmin(admin.ModelAdmin):
    inlines = (FactoryRecipeInline, FactoryNodeInline)
    exclude = ('key',)

class FactoryRecipeInline(admin.TabularInline):
    model = FactoryRecipe
    extra = 1

class FactoryAdmin(admin.ModelAdmin):
    inlines = (FactoryRecipeInline, )
    exclude = ('key',)

class ProductAdmin(admin.ModelAdmin):
    exclude = ('key',)

class MachineTypeAdmin(admin.ModelAdmin):
    exclude = ('key',)

class NodeTypeAdmin(admin.ModelAdmin):
    exclude = ('key',)

class NodeAdmin(admin.ModelAdmin):
    exclude = ('key',)

# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(MachineType, MachineTypeAdmin)
#admin.site.register(RecipeInput)
#admin.site.register(RecipeOutput)
admin.site.register(NodeType, NodeTypeAdmin)
admin.site.register(Factory, FactoryAdmin)
admin.site.register(Node, NodeAdmin)
admin.site.register(FactoryRecipe, FactoryRecipeAdmin)