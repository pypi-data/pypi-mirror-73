from django.db import models
import core.models


# Create your models here.
class Produto(core.models.Log):
    nome = models.CharField(max_length=200, null=True)
    tipo_produto = models.ForeignKey('produto.Tipo', on_delete=models.DO_NOTHING, null=True)
    fabricante = models.ForeignKey('fornecedor.Fabricante', on_delete=models.DO_NOTHING, null=True)

    grupo = models.ManyToManyField('produto.Grupo', through='produto.ProdutoGrupo', through_fields=('produto', 'grupo'))
    categoria = models.ManyToManyField('produto.Categoria', through='produto.ProdutoCategoria', through_fields=('produto', 'categoria'))
    kit = models.ManyToManyField('produto.Kit', through='produto.ProdutoKit', through_fields=('produto', 'kit'))
    bula = models.ManyToManyField('produto.Bula', through='produto.ProdutoBula', through_fields=('produto', 'bula'))
    tipo_receita = models.ManyToManyField('produto.TipoReceita', through='produto.ProdutoTipoReceita', through_fields=('produto', 'tipo_receita'))
    principio_ativo = models.ManyToManyField('produto.PrincipioAtivo', through='produto.ProdutoPrincipioAtivo', through_fields=('produto', 'principio_ativo'))
    especialidade = models.ManyToManyField('produto.Especialidade', through='produto.ProdutoEspecialidade', through_fields=('produto', 'especialidade'))

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto'


class Tipo(core.models.Log):
    nome = models.CharField(max_length=200, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_tipo'


class Grupo(core.models.Log):
    nome = models.CharField(max_length=200, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_grupo'


class ProdutoGrupo(core.models.Log):
    produto = models.ForeignKey('produto.Produto', on_delete=models.DO_NOTHING, null=True)
    grupo = models.ForeignKey('produto.Grupo', on_delete=models.DO_NOTHING, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_produtogrupo'


class Categoria(core.models.Log):
    nome = models.CharField(max_length=200, null=True)
    categoria_pai = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_categoria'


class ProdutoCategoria(core.models.Log):
    produto = models.ForeignKey('produto.Produto', on_delete=models.DO_NOTHING, null=True)
    categoria = models.ForeignKey('produto.Categoria', on_delete=models.DO_NOTHING, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_produtocategoria'


class Kit(core.models.Log):
    nome = models.CharField(max_length=200, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_kit'


class ProdutoKit(core.models.Log):
    produto = models.ForeignKey('produto.Produto', on_delete=models.DO_NOTHING, null=True)
    kit = models.ForeignKey('produto.Kit', on_delete=models.DO_NOTHING, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_produtokit'


class Bula(core.models.Log):
    nome = models.CharField(max_length=200, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_bula'


class ProdutoBula(core.models.Log):
    produto = models.ForeignKey('produto.Produto', on_delete=models.DO_NOTHING, null=True)
    bula = models.ForeignKey('produto.Bula', on_delete=models.DO_NOTHING, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_produtobula'


class TipoReceita(core.models.Log):
    nome = models.CharField(max_length=200, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_tiporeceita'


class ProdutoTipoReceita(core.models.Log):
    produto = models.ForeignKey('produto.Produto', on_delete=models.DO_NOTHING, null=True)
    tipo_receita = models.ForeignKey('produto.TipoReceita', on_delete=models.DO_NOTHING, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_produtotiporeceita'


class PrincipioAtivo(core.models.Log):
    nome = models.CharField(max_length=200, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_principioativo'


class ProdutoPrincipioAtivo(core.models.Log):
    produto = models.ForeignKey('produto.Produto', on_delete=models.DO_NOTHING, null=True)
    principio_ativo = models.ForeignKey('produto.PrincipioAtivo', on_delete=models.DO_NOTHING, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_produtoprincipioativo'


class Especialidade(core.models.Log):
    nome = models.CharField(max_length=200, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_especialidade'


class ProdutoEspecialidade(core.models.Log):
    produto = models.ForeignKey('produto.Produto', on_delete=models.DO_NOTHING, null=True)
    especialidade = models.ForeignKey('produto.Especialidade', on_delete=models.DO_NOTHING, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'produto_produtoespecialidade'