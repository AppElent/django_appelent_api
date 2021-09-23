from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from crum import get_current_user
User = get_user_model()

alphanumeric = RegexValidator(r'^[-0-9a-zA-Z ]*$', 'Only alphanumeric characters, spaces or dashes are allowed.')

class MachineType(models.Model):
    key = models.CharField(max_length=30, blank=True, primary_key=True)
    name = models.CharField(max_length=30,validators=[alphanumeric])
    power_usage = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.key = self.name.replace(' ', '_').lower()
        super(MachineType, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    key = models.CharField(max_length=30, blank=True, primary_key=True)
    name = models.CharField(max_length=30,validators=[alphanumeric])
    default_recipe = models.ForeignKey('Recipe' , on_delete=models.SET_NULL, null=True, blank=True, related_name='default_recipe_products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.key = self.name.replace(' ', '_').lower()
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    key = models.CharField(max_length=50, blank=True, primary_key=True)
    RecipeTypes = models.TextChoices('RecipeType', 'default alternate')
    name = models.CharField(max_length=50,validators=[alphanumeric])
    type = models.CharField(blank=True, choices=RecipeTypes.choices, max_length=20, default='default')
    machine = models.ForeignKey(MachineType, on_delete=models.CASCADE, related_name='recipes')
    products_input = models.ManyToManyField(Product, through='RecipeInput', related_name='products_input')
    products_output = models.ManyToManyField(Product, through='RecipeOutput',related_name='products_output')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.key = self.name.replace(' ', '_').lower()
        super(Recipe, self).save(*args, **kwargs)

    def __str__(self):
        return self.name + ' - ' + self.type

class RecipeInput(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.recipe.name + ' - ' + self.product.name + ' - ' + str(self.amount)

class RecipeOutput(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.recipe.name + ' - ' + self.product.name + ' - ' + str(self.amount)

class NodeType(models.Model):
    key = models.CharField(max_length=50, blank=True, primary_key=True)
    name = models.CharField(max_length=50,validators=[alphanumeric])
    NodeTypes = models.TextChoices('NodeTypes', 'Node Well')
    type = models.CharField(max_length=50, choices=NodeTypes.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.key = self.name.replace(' ', '_').lower()
        super(NodeType, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.name)

################### 

class Game(models.Model):
    key = models.CharField(max_length=50, blank=True, primary_key=True)
    name = models.CharField(max_length=50,validators=[alphanumeric])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.key = self.name.replace(' ', '_').lower()
        super(Factory, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class GamePlayer(models.Model):
    name = models.CharField(max_length=100)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='gameplayers')

class Factory(models.Model):
    key = models.CharField(max_length=100, blank=True, primary_key=True)
    name = models.CharField(max_length=50,validators=[alphanumeric])
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.key = self.game.name.replace(' ', '_').lower() + '__' +  self.name.replace(' ', '_').lower()
        super(Factory, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Node(models.Model):
    key = models.CharField(max_length=50, blank=True, primary_key=True)
    name = models.CharField(max_length=50,validators=[alphanumeric])
    type = models.ForeignKey(NodeType, on_delete=models.CASCADE, related_name='nodes')
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    purity_choices = [
        ('I', 'Impure'),
        ('N', 'Normal'),
        ('P', 'Pure'),
    ]
    purity = models.CharField(max_length=1, choices=purity_choices)
    CHOICES = [(i,i) for i in range(1, 4)]
    miner = models.IntegerField(default=1, choices=CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.key = self.game.name.replace(' ', '_').lower() + '__' +  self.name.replace(' ', '_').lower()
        super(Node, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class FactoryRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    depends_on_node = models.ManyToManyField(Node, blank=True, through='FactoryNodeAmount')
    depends_on_factoryrecipe = models.ManyToManyField('FactoryRecipe', blank=True, through='FactoryRecipeAmount')
    factory = models.ForeignKey(Factory, on_delete=models.CASCADE, related_name='factoryrecipes')
    amount = models.DecimalField(decimal_places=2,max_digits=5)	
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.factory.name + ' - ' + self.recipe.name + ' (' + str(self.amount) + ')'

class FactoryRecipeAmount(models.Model):
    recipe_from = models.ForeignKey(FactoryRecipe, on_delete=models.CASCADE, related_name='recipe_from')
    recipe_to = models.ForeignKey(FactoryRecipe, on_delete=models.CASCADE, related_name='recipe_to')
    amount = models.DecimalField(decimal_places=2,max_digits=5)	

class FactoryNodeAmount(models.Model):
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
    factoryrecipe = models.ForeignKey(FactoryRecipe, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2,max_digits=5)	