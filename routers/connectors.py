from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse

from pydantic import BaseModel
from typing import List, Optional

from engines.connectors import Connectors

router = APIRouter()


# / Models Dictionaries\

class ConnectorParameter (BaseModel):
    name: str
    display: str
    type: str
    required: bool
    hidden: bool


class ConnectorInstance (BaseModel):
    configName: str
    configURL: str
    configAPIID: str
    configAPISecret: str
    configInSecure: bool
    configProxy: bool
    enabled: bool


class Connector(BaseModel):
    ID: str
    Name: str
    DisplayName: str
    Version: str
    Description: str
    Image: str
    Path: str
    Parameters: List[ConnectorParameter]
    Instances: Optional[List[ConnectorInstance]]


class GetConnectorsResponse(BaseModel):
    Connectors: List[Connector]


class UploadConnectorResponse(BaseModel):
    message: str


class DeleteConnectorResponse(BaseModel):
    message: str


class FindConnectorResponse(BaseModel):
    category: str
    id: str
    name: str
    display: str
    version: str
    description: str
    image: str
    parameters: List[ConnectorParameter]
    connector: dict


class FindConnectorFailedResponse(BaseModel):
    message: str


class AddInstanceResponse(BaseModel):
    message: str


class DeleteInstanceResponse(BaseModel):
    message: str


class UpdateInstanceResponse(BaseModel):
    message: str


# / Request and Response Models\

class ConnectorsResponseModel(BaseModel):
    status: str
    payload: GetConnectorsResponse

    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "payload": {
                    "Connectors": [
                        {
                            "ID": "CNNMoney",
                            "Name": "CNN Money",
                            "DisplayName": "CNN Money Integration",
                            "Version": -1,
                            "Description": "An Integration to Query Stock Information",
                            "Image": "..TruncatedBase64",
                            "Path": "content/connectors/CNNMoney/CNNMoney.yml",
                            "Parameters": [
                                {
                                    "name": "url",
                                    "display": "URL",
                                    "required": True,
                                    "type": "string",
                                    "hidden": False
                                },
                                {
                                    "name": "insecure",
                                    "display": "Validate SSL",
                                    "required": False,
                                    "type": "boolean",
                                    "hidden": False
                                },
                                {
                                    "name": "proxy",
                                    "display": "Use Proxy",
                                    "required": False,
                                    "type": "boolean",
                                    "hidden": False
                                }
                            ],
                            "Instances": [
                                {
                                    "configName": "Instance1",
                                    "configURL": "",
                                    "configAPIID": "",
                                    "configAPISecret": "",
                                    "configInSecure": False,
                                    "configProxy": False,
                                    "enabled": False
                                }
                            ]
                        },
                        {
                            "ID": "ALPACA",
                            "Name": "ALPACA",
                            "DisplayName": "ALPACA Trading Platform",
                            "Version": -1,
                            "Description": "An Integration to Query Stock Information and Place Orders",
                            "Image": "..TruncatedBase64",
                            "Path": "content/connectors/ALPACA/ALPACA.yml",
                            "Parameters": [
                                {
                                    "name": "url",
                                    "display": "URL",
                                    "required": True,
                                    "type": "string",
                                    "hidden": False
                                },
                                {
                                    "name": "apiID",
                                    "display": "API ID",
                                    "required": True,
                                    "type": "string",
                                    "hidden": False
                                },
                                {
                                    "name": "apiSecret",
                                    "display": "API Secret",
                                    "required": False,
                                    "type": "string",
                                    "hidden": False
                                },
                                {
                                    "name": "insecure",
                                    "display": "Validate SSL",
                                    "required": False,
                                    "type": "boolean",
                                    "hidden": False
                                },
                                {
                                    "name": "proxy",
                                    "display": "Use Proxy",
                                    "required": False,
                                    "type": "boolean",
                                    "hidden": False
                                }
                            ],
                            "Instances": []
                        }
                    ]
                }
            }
        }


class ConnectorUploadModel(BaseModel):
    status: str
    payload:UploadConnectorResponse

    class Config:

        schema_extra = {
            "example": {
                "status": "success",
                "payload": {
                    "message": "Connector successfully registered .."
                }
            }
        }


class ConnectorUploadFailedModel(BaseModel):
    status: str
    payload: UploadConnectorResponse

    class Config:

        schema_extra = {
            "example": {
                "status": "fail",
                "payload": {
                    "message": "Error (C:3) Connector already exists .."
                }
            }
        }


class ConnectorDeleteModel(BaseModel):
    status: str
    payload: DeleteConnectorResponse

    class Config:

        schema_extra = {
            "example": {
                "status": "success",
                "payload": {
                    "message": "Connector successfully deleted .."
                }
            }
        }


class ConnectorDeleteFailedModel(BaseModel):
    status: str
    payload: DeleteConnectorResponse

    class Config:

        schema_extra = {
            "example": {
                "status": "fail",
                "payload": {
                    "message": "Error (C:8) Connector not found .."
                }
            }
        }


class ConnectorFindModel(BaseModel):
    status: str
    payload: FindConnectorResponse

    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "payload": {
                    "category": "Trading Platforms",
                    "id": "Yahoo",
                    "name": "Yahoo",
                    "display": "Yahoo Integration",
                    "version": -1,
                    "description": "An Integration to Query Stock Information",
                    "image": "TruncatedBase64",
                    "parameters": [
                        {
                            "name": "url",
                            "display": "URL",
                            "required": True,
                            "type": "string",
                            "hidden": True
                        },
                        {
                            "name": "apiID",
                            "display": "API ID",
                            "required": True,
                            "type": "string",
                            "hidden": False
                        },
                        {
                            "name": "apiSecret",
                            "display": "API Secret",
                            "required": False,
                            "type": "string",
                            "hidden": False
                        },
                        {
                            "name": "insecure",
                            "display": "Validate SSL",
                            "required": False,
                            "type": "boolean",
                            "hidden": False
                        },
                        {
                            "name": "proxy",
                            "display": "Use Proxy",
                            "required": False,
                            "type": "boolean",
                            "hidden": False
                        }
                    ],
                    "connector": {
                        "commands": [
                            {
                                "name": "yahoo-get-account-information",
                                "deprecated": False,
                                "description": "Get Alpaca Account Information",
                                "execution": False,
                                "outputs": [
                                    {
                                        "contextPath": "Alpaca.Account",
                                        "description": "Alpaca Acount Information",
                                        "type": "String"
                                    }
                                ]
                            }
                        ],
                        "code": "Truncated",
                        "dockerimage": "wave/alpaca:1.0",
                        "feed": False,
                        "running": False
                    }
                }
            }
        }


class ConnectorFindFailedModel(BaseModel):
    status: str
    payload: FindConnectorFailedResponse

    class Config:

        schema_extra = {
            "example": {
                "status": "fail",
                "payload": {
                    "message": "Error (C:1) Connector not found .."
                }
            }
        }


class InstanceConfigModel(BaseModel):
    configName: str
    configURL: Optional[str]
    configAPIID: Optional[str]
    configAPISecret: Optional[str]
    configInSecure: bool
    configProxy: bool
    enabled: bool

    class Config:

        schema_extra = {
            "example": {
                "configName": "Instance1",
                "configAPIID": "test",
                "configAPISecret": "",
                "configURL": "",
                "configProxy": True,
                "configInSecure": False,
                "enabled": True
            }
        }


class InstanceAddModel(BaseModel):
    status: str
    payload: AddInstanceResponse

    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "payload": {
                    "message": "Config successfully saved .."
                }
            }
        }


class InstanceAddFailedModel(BaseModel):
    status: str
    payload: AddInstanceResponse

    class Config:

        schema_extra = {
            "example": {
                "status": "fail",
                "payload": {
                    "message": "Error (C:9) Connector not found .."
                }
            }
        }


class InstanceDeleteModel(BaseModel):
    status: str
    payload: DeleteInstanceResponse

    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "payload": {
                    "message": "Instance successfully deleted .."
                }
            }
        }


class InstanceDeleteFailedModel(BaseModel):
    status: str
    payload: DeleteInstanceResponse

    class Config:

        schema_extra = {
            "example": {
                "status": "fail",
                "payload": {
                    "message": "Error (C:10) Instance not found .."
                }
            }
        }


class InstanceConfigUpdateModel(BaseModel):
    configName: Optional[str]
    configURL: Optional[str]
    configAPIID: Optional[str]
    configAPISecret: Optional[str]
    configInSecure: Optional[bool]
    configProxy: Optional[bool]
    enabled: Optional[bool]

    class Config:

        schema_extra = {
            "example": {
                "configAPIID": "test"
            }
        }


class InstanceUpdateModel(BaseModel):
    status: str
    payload: UpdateInstanceResponse

    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "payload": {
                    "message": "Instance successfully updated .."
                }
            }
        }


class InstanceUpdateFailedModel(BaseModel):
    status: str
    payload: UpdateInstanceResponse

    class Config:

        schema_extra = {
            "example": {
                "status": "fail",
                "payload": {
                    "message": "Error (C:11) Instance not found .."
                }
            }
        }


# / EndPoints \

@router.get("/api/connectors", response_model=ConnectorsResponseModel, tags=["connectors"])
async def return_connectors():
    return Connectors.get_connectors()


@router.post("/api/connector/", response_model=ConnectorUploadModel, responses={409: {"model": ConnectorUploadFailedModel}}, tags=["connectors"])
async def upload_connector(connector: UploadFile = File(...)):
    received_content = await connector.read()
    response = Connectors.register_connector(connector, received_content)
    if response.get('status') == 'success':
        return response
    else:
        return JSONResponse(status_code=409, content=response)


@router.delete("/api/connector/{connector_id}", response_model=ConnectorDeleteModel, responses={404: {"model": ConnectorDeleteFailedModel}}, tags=["connectors"])
async def delete_connector(connector_id: str):
    response = Connectors.delete_connector(connector_id)
    if response.get('status') == 'success':
        return response
    else:
        return JSONResponse(status_code=404, content=response)


@router.get("/api/connector/{connector_id}", response_model=ConnectorFindModel, responses={404: {"model": ConnectorFindFailedModel}}, tags=["connectors"])
async def return_connector(connector_id: str):
    response = Connectors.find_connector(connector_id)
    if response.get('status') == 'success':
        return response
    else:
        return JSONResponse(status_code=404, content=response)


@router.post("/api/connectors/{connector_id}/config", response_model=InstanceAddModel, responses={404: {"model": InstanceAddFailedModel}}, tags=["connectors"])
async def create_instance(connector_id: str, config: InstanceConfigModel):
    response = Connectors.add_instance(connector_id, config)
    if response.get('status') == 'success':
        return response
    else:
        return JSONResponse(status_code=404, content=response)


@router.delete("/api/connectors/{connector_id}/config/{instance_name}", response_model=InstanceDeleteModel, responses={404: {"model": InstanceDeleteFailedModel}}, tags=["connectors"])
async def delete_instance(connector_id: str, instance_name: str):
    response = Connectors.delete_instance(connector_id, instance_name)
    if response.get('status') == 'success':
        return response
    else:
        return JSONResponse(status_code=404, content=response)


@router.put("/api/connectors/{connector_id}/config/{instance_name}", response_model=InstanceUpdateModel, responses={404: {"model": InstanceUpdateFailedModel}}, tags=["connectors"])
async def update_instance(connector_id: str, instance_name: str, instance_update: InstanceConfigModel):
    response = Connectors.update_instance(connector_id, instance_name, instance_update)
    if response.get('status') == 'success':
        return response
    else:
        return JSONResponse(status_code=404, content=response)