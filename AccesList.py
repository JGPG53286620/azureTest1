from msal import ConfidentialClientApplication
import requests
import json

def connectSharepoint():
    client_id = "24da34e3-84eb-49ff-82fd-5e558e64ce34"
    tenant_id= "7266cf60-2a18-461e-9a40-171f83b02de5"
    authority = f"https://login.microsoftonline.com/{tenant_id}"

    client_secret="Yl~8Q~HHjI5qhEFaSdvEsQb~3LgYf~XlqnaC6bcG" #no borrar

    #scope=["https://graph.microsoft.com/.default"]
    scope= ["https://glouphi.sharepoint.com/.default"]

    cert_thumbprint="38FDE1F88CC23C60C309055B261B6ACA4BE53CA9"
    private_key="""-----BEGIN PRIVATE KEY-----
                MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQD1RNXlM9VeIpIy
                poatalU4MdTTs6YHw81mdLN6x4tCexOw/2yL+qZW8cDzaxwfJ6YbnDzXeIc6NHba
                1vgoSop6TVSmLh4W4gXSbfqSSWsyYI1E0tua+LkjU4/J/6Khn02QcRNnkVmYjjKH
                oWNZAAZdj/O7YkQLXqd3U5B+uqSFC1H0rqjdj9nHUygl0kPlSFVYja1lnjKD/X/g
                dyA2ZQzyaeVbE1fWtM0xIjN38Nz2XoMxCfNByonAisRG85OYRmTSiaAzDx/0tLrH
                tgQc3KmY9QIvmnvYZrEJ8JYe50EDsLzMLAxM7C62cO8bf613cc1ImkfpAjFFGt4o
                HySF0rD1AgMBAAECggEAO+bR7qaYJ+N9nU06e0QLCCxzdDjeBet2UN2TsBroEhaJ
                GqNnWVCgK3/jxg+U0K8YTIn9+gn/zOFfXdc+yGhcJb6ZO/TreF8/WMNvfSbdPXKD
                ThnJdLHmVZBk/8qlZ5/Gi85yFMtU/INOJ/3si6IL6/Hqbwty3uwBLo2ELs9auvss
                Y/DwiD1qTbVPDkkWAAh7GQKsVkP3ez4ZaaUt0v2l1oJvPdJ4i4qJJQ0eybwtp+17
                0vgbHAOXmvj/TSz/I5Fj6dyN9sMrqXdRWMq6xD2pj2iFOSFkNl/yk7sljR6Pci1m
                m/NM6SozTlKOTANLaFfKzdqxP7/hccS2vjzBFc1igQKBgQD8wN5HiUTf71qPilFF
                +5x4qDPocuaCW8guASvp8eWE6gXklo7uuAIV1wM6PKwo0EHESk4xQW55uKUNDj9h
                9O3hu6Vttt60PY9GYiFaGv/NsGVY2HgT5QwrwGgim6f/ozgpYpOKb+ADwp2zL3GT
                hUtBVba95VZF6z21tTBkA9DyxQKBgQD4a1saxt/vdihwHfsNsmucsGLldwPbCJxf
                60ejR6xltQaJvHX6aMPZz0nvnxZlEqU147IYn30cwMdCPRTbSx1HUNiezrM2glm1
                x02Hovq9Ls44TONuo8v/teF8PbxBZaO3DrghMDLVcK0wv8pLyfyHMC+WxT6xdVbM
                2iJLpZHocQKBgQC8TgzMiw5PMAnuSwSF+RD4K4iQs5ncoPignarT3q46uget6CWQ
                4HJdRxVWfAFfXtjAnwNmWvMtqEz/TxAVsN7RgHWdKdL9wadOrqleciMGYVcAPDYp
                zEmnBvAOaJ1fLYEYBCMbzoG9C29mIgCiAXqxsGQ3UfdWnA4bpGPq/5TaaQKBgQCJ
                CO+gvcQaHFwCPQeYbqveK47iddyynvVkFC3YbFk1Yb7RjByondIr/KUUgfWgm8B3
                EbvUyWYCznUcnQU8Uxs7k+Vq9Sr3DsDd/atO/yDB62fmtsNe7QxDatmP555JlP/S
                o1P/Os9P3nArTCET3cBn8rTNvtDuo4PWTR5ODG+IgQKBgHt1NJm9GRKU2gdlJeaO
                5tliluRtYNXTH1t5iWYs38FiGisIpCSjOkkmCuwgo8WSdYi2AvYdevX54tn31+g4
                HTz4uOJAq2uvmY3qrWqUFj1MC3za3ml0AU1vnEmtkIJO8O5WIscr3Ff7Zo/FIdrw
                UmDwCiZNzlmdpZRpVn60Ipfy
                -----END PRIVATE KEY-----"""

    cert={
        "private_key":private_key,
        "thumbprint":cert_thumbprint,
    }

    app=ConfidentialClientApplication(
        client_id=client_id,
        authority=authority,
        client_credential=client_secret
    )

    result = app.acquire_token_for_client(scopes=scope)

    sharepoint_base_url= "https://glouphi.sharepoint.com/sites/Data_lake"
    final_url=f"{sharepoint_base_url}/_api/web/sitegroups"

    if "access_token" in result:
        access_token=result["access_token"]
    
    headers={
        "Authorization" : f"Bearer {access_token}",
        "Accept" : "application/json;odata=verbose",
        "Content-Type" : "application/json"
    }

    response = requests.get(url=final_url, headers=headers)
    return "executed succsesfully with response: "+str(response)