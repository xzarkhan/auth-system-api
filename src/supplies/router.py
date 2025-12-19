from fastapi import APIRouter, Depends

from src.auth.dependencies import PermissionDep


router = APIRouter(prefix="/supplies", tags=["Supplies"])


@router.get(
    "",
    dependencies=[
        Depends(
            PermissionDep(["supplies:read", "supplies:full_access"], required_all=False)
        )
    ],
)
async def get_all_supplies():
    return [{"supply_1": "data"}, {"supply_2": "data"}, {"supply_3": "data"}]


@router.get(
    "/{supply_id}",
    dependencies=[
        Depends(
            PermissionDep(["supplies:read", "supplies:full_access"], required_all=False)
        )
    ],
)
async def get_supply_by_id():
    return {"supply": "data"}


@router.post(
    "/{supply_id}",
    dependencies=[
        Depends(
            PermissionDep(["supplies:create", "supplies:full_access"], required_all=False)
        )
    ],
)
async def create_supply():
    return {"new_supply": "data"}


@router.patch(
    "/{supply_id}",
    dependencies=[
        Depends(
            PermissionDep(["supplies:update", "supplies:full_access"], required_all=False)
        )
    ],
)
async def partial_update_supply():
    return {"partial_updated_supply": "data"}


@router.put(
    "/{supply_id}",
    dependencies=[
        Depends(
            PermissionDep(["supplies:update", "supplies:full_access"], required_all=False)
        )
    ],
)
async def update_supply():
    return {"updated_supply": "data"}


@router.delete(
    "/{supply_id}",
    dependencies=[
        Depends(
            PermissionDep(["supplies:delete", "supplies:full_access"], required_all=False)
        )
    ],
)
async def delete_supply():
    return {"deleted_supply": "data"}
