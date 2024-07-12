from fastapi import APIRouter, status, Body
from src.contrib.repository.dependencies import DatabaseDependencys
from src.atleta.schemas import AtletaIn, AtletaOut, AtletaUpdate
from pydantic import UUID4
from src.atleta.models import AtletaModel
from src.categorias.models import CategoriaModel
from src.centro_treinamento.models import CentroTreinamentoModel

router = APIRouter()

@router.post(
  '/', 
  summary = 'Criar um novo atleta',
  status_code=status.HTTP_201_CREATED,
  response_model=AtletaOut
)
async def post(
  db_session: DatabaseDependencys, 
  atleta_in: AtletaIn = Body(...)):

  categoria_name = atleta_in.categoria.nome
  categoria = (await db_session.execute(select(CategoriaModel).filter_by(nome=categoria_name))).scalars.all()
  
  if not categoria:
    raise HYYPException(
      status_code=status.HTTP_404_BAD_REQUEST,
      detail=f"A categoria {categoria_name} não foi encontrada."
    )

  centro_treinamento_name = atleta_in.centro_treinamento.nome
  centro_treinamento = (await db_session.execute(select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_name))).scalars.all()
  
  if not centro_treinamento:
    raise HYYPException(
      status_code=status.HTTP_404_BAD_REQUEST,
      detail=f"O centro de treinamento {centro_treinamento_name} não foi encontrado."
    )
  try:
    atleta_out = AtletaOut(id=uuid4(), created_at=datetime.utcnow(), **atleta_in.model_dump())
    atleta_model = AtletaModel(**atleta_out.model_dump(exclude={'categoria','centro_treinamento'}))
    atleta_model.categoria_id = categoria.pk_id
    atleta_model.centro_treinamento_id = centro_treinamento.pk_id

    db_session.add(atleta_model)
    await db_session.commit()
  except Exception:
    raise HYYPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail=f"Ocorreu um erro ao inserir os dados no banco."
    )
  return atleta_out

@router.get(
  '/', 
  summary = 'Consultar todos os atletas',
  status_code=status.HTTP_200_OK,
  response_model=list[AtletaOut]
)
async def query(db_session: DatabaseDependencys) -> list[AtletaOut]:
  atletas: list[AtletaOut] = (await db_session.execute(select(AtletaModel))).scalars().all()
  return [AtletaOut.model_validate(atleta) for atleta in atletas]

@router.get(
  '/{id}', 
  summary = 'Consultar atleta pelo id',
  status_code=status.HTTP_200_OK,
  response_model=AtletaOut,
)
async def query(id: UUID4, db_session: DatabaseDependencys) -> AtletaOut:
  atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
  
  if not atleta:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atleta não encontrado no id:{id}")

  return atleta

@router.patch(
  '/{id}', 
  summary = 'Editar atleta pelo id',
  status_code=status.HTTP_200_OK,
  response_model=AtletaOut,
)
async def query(id: UUID4, db_session: DatabaseDependencys, atleta_up: AtletaUpdate = Body(...)) -> AtletaOut:
  atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
  
  if not atleta:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atleta não encontrado no id:{id}")
  
  atleta_update = atleta_up.model_dump(exclude_unset=True)
  for key, value in atleta_update.items():
    setattr(atleta, key, value)
  await db_session.commit()
  await db_session.refresh(atleta)
  
  return atleta


@router.delete(
  '/{id}', 
  summary = 'deletar um atleta pelo id',
  status_code=status.HTTP_204_NO_CONTENT
)
async def query(id: UUID4, db_session: DatabaseDependencys) -> None:
  atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
  
  if not atleta:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atleta não encontrado no id:{id}")
  
  await db_session.delete(atleta)
  await db_session.commit()
