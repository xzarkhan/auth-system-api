from fastapi import APIRouter, Depends

from src.auth.dependencies import PermissionDep


router = APIRouter(prefix="/products", tags=["Products"])


@router.get(
    "",
    dependencies=[
        Depends(
            PermissionDep(["products:read", "products:full_access"], required_all=False)
        )
    ],
)
async def get_all_products():
    return [{"product_1": "data"}, {"product_2": "data"}, {"product_3": "data"}]


@router.get(
    "/{product_id}",
    dependencies=[
        Depends(
            PermissionDep(["products:read", "products:full_access"], required_all=False)
        )
    ],
)
async def get_product_by_id():
    return {"product": "data"}


@router.get(
    "",
    dependencies=[
        Depends(
            PermissionDep(["products:create", "products:full_access"], required_all=False)
        )
    ],
)
async def create_product():
    return {"new_product": "data"}
