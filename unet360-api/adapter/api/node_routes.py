from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Optional, Any

from adapter.database.node_repository import NodeRepository
from adapter.database.location_repository import LocationRepository
from adapter.database.tag_repository import TagRepository

from core.dtos.responses_dto import GeneralResponse 
from core.services.node_service import NodeService
from core.dtos.node_dto import NodeCreateDTO, NodeOutDTO, NodeUpdateDTO, NodeStatusDTO

from core.dependencies.auth_dependencies import get_current_admin_user

router = APIRouter(prefix="/nodes", tags=["Nodes"])

service = NodeService(NodeRepository(), LocationRepository(), TagRepository()) 

@router.get("/statuses", response_model=GeneralResponse)
async def get_nodes_statuses():
    try:
        statuses = await service.get_nodes_statuses()
        return GeneralResponse(
            http_code=status.HTTP_200_OK,
            status=True,
            response_obj=[s.model_dump() for s in statuses]
        )
    except HTTPException as e:
        return GeneralResponse(
            http_code=e.status_code,
            status=False,
            response_obj={"message": e.detail}
        )
    except Exception as e:
        return GeneralResponse(
            http_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            status=False,
            response_obj={"message": f"An unexpected error occurred: {str(e)}"}
        )

@router.post("/", response_model=GeneralResponse)
async def create_node(dto: NodeCreateDTO, 
                      current_user_id: str = Depends(get_current_admin_user)): 
    try:
        created_node_dto = await service.create_node(dto) 
        
        return GeneralResponse(
            http_code=status.HTTP_201_CREATED,
            status=True,
            response_obj=created_node_dto.model_dump()
        )
    except HTTPException as e:
        return GeneralResponse(
            http_code=e.status_code,
            status=False,
            response_obj={"message": e.detail}
        )
    except Exception as e:
        return GeneralResponse(
            http_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            status=False,
            response_obj={"message": f"An unexpected error occurred: {str(e)}"}
        )

@router.get("/{name}", response_model=GeneralResponse)
async def get_node(name: str):
    try:
        node_out_dto = await service.get_node_by_name(name)
        
        return GeneralResponse(
            http_code=status.HTTP_200_OK,
            status=True,
            response_obj=node_out_dto.model_dump() if node_out_dto else None
        )
    except HTTPException as e:
        return GeneralResponse(
            http_code=e.status_code,
            status=False,
            response_obj={"message": e.detail}
        )
    except Exception as e:
        return GeneralResponse(
            http_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            status=False,
            response_obj={"message": f"An unexpected error occurred: {str(e)}"}
        )

@router.get("/", response_model=GeneralResponse)
async def get_all_nodes():
    try:
        nodes_out_dtos = await service.get_all_nodes()
        
        nodes_data_list = [node_dto.model_dump() for node_dto in nodes_out_dtos]
        return GeneralResponse(
            http_code=status.HTTP_200_OK,
            status=True,
            response_obj=nodes_data_list
        )
    except HTTPException as e:
        return GeneralResponse(
            http_code=e.status_code,
            status=False,
            response_obj={"message": e.detail}
        )
    except Exception as e:
        return GeneralResponse(
            http_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            status=False,
            response_obj={"message": f"An unexpected error occurred: {str(e)}"}
        )
@router.get("/{name}", response_model=GeneralResponse)
async def get_node(name: str):
    try:
        node_out_dto = await service.get_node_by_name(name)
        
        return GeneralResponse(
            http_code=status.HTTP_200_OK,
            status=True,
            response_obj=node_out_dto.model_dump() if node_out_dto else None
        )
    except HTTPException as e:
        return GeneralResponse(
            http_code=e.status_code,
            status=False,
            response_obj={"message": e.detail}
        )
    except Exception as e:
        return GeneralResponse(
            http_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            status=False,
            response_obj={"message": f"An unexpected error occurred: {str(e)}"}
        )

@router.patch("/{name}", response_model=GeneralResponse)
async def update_node(name: str, dto: NodeUpdateDTO, 
                      current_user_id: str = Depends(get_current_admin_user)):
    try:
        updated_node_dto = await service.update_node(name, dto)
        
        return GeneralResponse(
            http_code=status.HTTP_200_OK,
            status=True,
            response_obj=updated_node_dto.model_dump()
        )
    except HTTPException as e:
        return GeneralResponse(
            http_code=e.status_code,
            status=False,
            response_obj={"message": e.detail}
        )
    except Exception as e:
        return GeneralResponse(
            http_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            status=False,
            response_obj={"message": f"An unexpected error occurred: {str(e)}"}
        )

@router.delete("/{name}", response_model=GeneralResponse)
async def delete_node(name: str, 
                      current_user_id: str = Depends(get_current_admin_user)):
    try:
        delete_result = await service.delete_node(name)
        
        return GeneralResponse(
            http_code=status.HTTP_200_OK, 
            status=True,
            response_obj=delete_result
        )
    except HTTPException as e:
        return GeneralResponse(
            http_code=e.status_code,
            status=False,
            response_obj={"message": e.detail}
        )
    except Exception as e:
        return GeneralResponse(
            http_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            status=False,
            response_obj={"message": f"An unexpected error occurred: {str(e)}"}
        )

