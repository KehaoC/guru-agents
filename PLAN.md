# Addtional Info
Upload attachments
Upload attachments, upload attachments in a multi-dimensional table in 2 steps

1.CallUpload media or Upload media in blocks interface upload file, upload success after obtaining the file fille_token

2.Call CreateRecord or UpdateRecord to update files to records;

Request body
```
{
    "records": [
        {
            "fields": {
            "Attachment": [
                {"file_token": "boxbcCFb2dBwMK9S8kDILk1tayh"},
                {"file_token": "boxbcCFb2dBwMK9S8kDILk1tayh"}
                ]
             }
        },
        {
            "fields": {
            "Attachment": [
                {"file_token": "boxbcCFb2dBwMK9S8kDILk1tayh"},
                {"file_token": "boxbcCFb2dBwMK9S8kDILk1tayh"}
                ]
             }
        }

     ]

}
```

# Upload Media
# Upload Media

Uploads a media file such as file, picture, and video to the specified cloud document. The media file will not be displayed in the user's Space, but only in the corresponding cloud document.

## Limitations

- The media file size must not exceed 20 MB. To upload files larger than 20 MB, you need to use the shard upload media-related interfaces. For details, refer to [Media overview](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/drive-v1/media/introduction).
- This interface supports a maximum call frequency of 5 QPS, 10,000 calls per day.

## Request

Facts | 
---|---
HTTP URL | https://open.feishu.cn/open-apis/drive/v1/medias/upload_all
HTTP Method | POST
Rate Limit | [Special Rate Limit](https://open.feishu.cn/document/ukTMukTMukTM/uUzN04SN3QjL1cDN)
Supported app types | Custom App、Store App
Required scopes<br>**To use this API, you must have at least 1 of the listed scopes.**<br>Enable any scope from the list | View, comment, edit and manage Base(bitable:app)<br>View, comment, edit, and manage Docs(docs:doc)<br>Upload image and file to document(docs:document.media:upload)<br>View, comment, edit, and manage all files in My Space(drive:drive)<br>View, comment, edit, and manage Sheets(sheets:spreadsheet)

### Request header

Parameter | Type | Required | Description
---|---|---|---
Authorization | string | Yes | `tenant_access_token`<br>or<br>`user_access_token`<br>**Value format**: "Bearer `access_token`"<br>**Example value**: "Bearer u-7f1bcd13fc57d46bac21793a18e560"<br>[How to choose and get access token](https://open.feishu.cn/document/uAjLw4CM/ugTN1YjL4UTN24CO1UjN/trouble-shooting/how-to-choose-which-type-of-token-to-use)
Content-Type | string | Yes | **Example value**: "multipart/form-data; boundary=---7MA4YWxkTrZu0gW"

### Request body

Parameter | Type | Required | Description
---|---|---|---
file_name | string | Yes | File name.<br>**Example value**: "demo.jpeg"<br>**Data validation rules**:<br>- Maximum length: `250` characters
parent_type | string | Yes | Upload point type, that is, to upload a certain type of media to the specified type of Docs. For example, if you insert a picture into the Upgraded Docs, then `parent_type` needs to be filled in as `docx_image` , and then if you upload an attachment to the Upgraded Docs, then `parent_type` needs to be filled in as `docx_file`.<br>**Example value**: "doc_image"<br>**Optional values are**:<br>- doc_image：Image of a document.<br>- docx_image：Upgraded docs image.<br>- sheet_image：Image of a sheet.<br>- doc_file：Doc file.<br>- docx_file：Upgraded docs file.<br>- sheet_file：Sheet file.<br>- vc_virtual_background：VC virtual background (This feature is under canary release).<br>- bitable_image：Image of a bitable.<br>- bitable_file：Bitable file.<br>- moments：Moments (This feature is under canary release).<br>- ccm_import_open：File to import into Docs.
parent_node | string | Yes | The `parent_node` is used to specify the specific document or location to which the media will be uploaded. Click [here](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/drive-v1/media/introduction) for an explanation of each `parent_type` and its corresponding `parent_node`.
size | int | Yes | The file size in bytes.<br>**Example value**: 1024<br>**Data validation rules**:<br>- Maximum value: `20971520`
checksum | string | No | Adler-32 checksum of the file. This field is optional.<br>**Example value**: "3248270248"
extra | string | No | The upload points in the following scenarios need to pass the token of the cloud document where the material is located through this parameter. The format of the extra parameter is `"{\"drive_route_token\":\"token of the cloud document where the material is located\"}"`. For details, refer to [Material Overview](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/drive-v1/media/introduction).<br>**Example value**: "{\"drive_route_token\":\"doxcnXgNGAtaAraIRVeCfmabcef\"}"
file | file | Yes | Binary content of the file.<br>**Example value**: file binary

### cURL example
```
curl --location --request POST 'https://open.feishu.cn/open-apis/drive/v1/medias/upload_all' \
--header 'Authorization: Bearer t-43b270c035ddffdcf79c9eb548d06318ca4abcef' \
--form 'file_name="demo.jpeg"' \
--form 'parent_type="doc_image"' \
--form 'parent_node="doccnFivLCfJfblZjGZtxgabcef"' \
--form 'size="1024"' \
--form 'file=@"/Path/demo.jpeg"'
--form 'extra="{\"drive_route_token\":\"doxcnXgNGAtaAraIRVeCfmabcef\"}"'
```

### Python example
```python
import os
import requests
from requests_toolbelt import MultipartEncoder

def upload_media():
    file_path = "path/demo.jpeg"
    file_size = os.path.getsize(file_path)
    url = "https://open.feishu.cn/open-apis/drive/v1/medias/upload_all"
    form = {'file_name': 'demo.jpeg',
            'parent_type': 'doc_image',
            'parent_node': 'doccnFivLCfJfblZjGZtxgabcef',
            'size': str(file_size),
            'file': (open(file_path, 'rb'))}  
    multi_form = MultipartEncoder(form)
    headers = {
        'Authorization': 'Bearer t-e13d5ec1954e82e458f3ce04491c54ea8c9abcef',  ## replace with real tenant_access_token
    }
    headers['Content-Type'] = multi_form.content_type
    response = requests.request("POST", url, headers=headers, data=multi_form)

if __name__ == '__main__':
    upload_media()
```

### Request body example

```HTTP
---7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="file_name";

demo.jpeg
---7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="parent_type";

doc_image
---7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="parent_node";

---7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="size";

1024
---7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="checksum";

3248270248
---7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="extra";

{\"drive_route_token\":\"doxcnXgNGAtaAraIRVeCfmabcef\"}
---7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="file";
Content-Type: application/octet-stream

file binary
---7MA4YWxkTrZu0gW
```

## Response

### Response body

Parameter | Type | Description
---|---|---
code | int | Error codes, fail if not zero
msg | string | Error descriptions
data | \- | \-
file_token | string | Token of the new file

### Response body example
```json
{
    "code": 0,
    "msg": "success",
    "data": {
        "file_token": "boxcnrHpsg1QDqXAAAyachabcef"
    }
}
```

### Error code

HTTP status code | Error code | Description | Troubleshooting suggestions
---|---|---|---
200 | 1061001 | internal error. | Internal service error, such as timeout or failure in processing error codes.
400 | 1061002 | params error. | Check whether the request parameters are correct.
404 | 1061003 | not found. | Check whether the resource exists.
403 | 1061004 | forbidden. | Confirm whether the current access identity has permission to read or edit files or folders. Please refer to the following methods to resolve this:<br>- When uploading materials, please ensure that the current caller has edit permissions for the target cloud document.<br>- When uploading files, please ensure that the current caller has edit permissions for the folder.<br>- When performing operations such as adding, deleting, or modifying files or folders, please ensure that the caller has sufficient document permissions:<br>- For the "create file" interface, the caller needs edit permissions for the target folder.<br>- For the "copy file" interface, the caller needs read or edit permissions for the file and edit permissions for the target folder.<br>- For the "move file" interface, the caller must have the following permissions:<br>- Manage permission for the document or folder being moved. <br>- Edit permission for current location of the document or folder.<br>- Edit permission for the new location.<br>- For the "delete file" interface, the caller must have one of the following two permissions:<br>- The app or user is the owner of the file and has edit permissions for the parent folder where the file is located.<br>- The app or user is not the owner of the file, but the owner of the parent folder where the file is located or has full access to the parent folder.<br>For information on how to grant permissions, refer to [How to Grant Permissions for Cloud Document Resources to an App](https://open.feishu.cn/document/uAjLw4CM/ugTN1YjL4UTN24CO1UjN/trouble-shooting/how-to-add-permissions-to-app).
401 | 1061005 | auth failed. | Assume the correct user or app mode to access the API.
200 | 1061006 | internal time out. | Internal service timeout. Please try again later.
404 | 1061007 | file has been delete. | Check whether the node has been deleted.
400 | 1061008 | invalid file name. | Check whether the file name has reached the maximum length or is empty.
400 | 1061021 | upload id expire. | The upload transaction has expired. Please upload again.
400 | 1061041 | parent node has been deleted. | Check whether the upload point has been deleted.
400 | 1061042 | parent node out of limit. | The number of media to upload to the current upload node has reached the limit. Please change the upload point.
400 | 1061043 | file size beyond limit. | Check whether the length of the file is within the limit. For more information, see [File size limits in Drive](https://www.feishu.cn/hc/zh-CN/articles/360049067549).
400 | 1061044 | parent node not exist. | `parent_node` does not exist. Please verify if the upload point token is incorrect:<br>- For the file upload interface, refer to [Folder Token Retrieval Method](https://open.feishu.cn/document/ukTMukTMukTM/ugTNzUjL4UzM14CO1MTN/folder-overview#-717d325) to ensure the correct folder token is provided.<br>- For the media upload interface, refer to [Upload Point Types and Upload Point Token](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/drive-v1/media/introduction#cc82be3c) to verify if the `parent_node` is correctly filled out.
200 | 1061045 | can retry. | Internal error. Please try again later.
400 | 1061109 | file name cqc not passed. | Make sure that the file to upload and the file name meet compliance.
400 | 1061113 | file cqc not passed. | Make sure that the file to upload and the file name meet compliance.
400 | 1061101 | file quota exceeded. | The tenant has reached the maximum capacity. Make sure that the tenant has sufficient capacity and then upload again.
202 | 1062004 | cover generating. | Generating thumbnails. Please try again later.
202 | 1062005 | file type not support cover. | The system cannot generate thumbnails for this type of file.
202 | 1062006 | cover no exist. | Generating thumbnails. Please try again later.
400 | 1062007 | upload user not match. | Make sure that the current request is sent by the same user or app as the upload task.
400 | 1062008 | checksum param Invalid. | Make sure that the checksum of the file or file block is correct.
400 | 1062009 | the actual size is inconsistent with the parameter declaration size. | The size of the file to transfer is inconsistent with that specified in the parameter.
400 | 1062010 | block missing, please upload all blocks. | Some file blocks are missing. Make sure that all file blocks are uploaded.
400 | 1062011 | block num out of bounds. | The number of file blocks to upload has reached the limit. Make sure that the file blocks belong to the specified file.
400 | 1061547 | attachment parent-child relation number exceed. | The media to upload to Docs has reached the limit.
400 | 1061061 | user quota exceeded. | You have reached your maximum personal capacity. Make sure that you have sufficient capacity and then upload again.
403 | 1061073 | no scope auth. | You have no access to the API.
400 | 1062012 | file copying. | Copying the file.
400 | 1062013 | file damaged. | Failed to copy the file.
403 | 1062014 | dedupe no support. | Instant transfer is not allowed.
400 | 1062051 | client connect close. | Disconnected from the client.
400 | 1062505 | parent node out of size. | The single tree in My Space has reached the maximum size of 400,000.
400 | 1062506 | parent node out of depth. | My Space supports up to 15 levels of directories.
400 | 1062507 | parent node out of sibling num. | The number of nodes mounted to the directory in My Space has reached the limit of **1,500** nodes per level.

# Create a record
# Create a record

Create a record

For the first access, please refer to [Cloud Document Interface QuickStart](https://open.feishu.cn/document/ukTMukTMukTM/uczNzUjL3czM14yN3MTN) & [Base OpenAPI Access Guide](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/bitable/notification) 

## Request

Facts | 
---|---
HTTP URL | https://open.feishu.cn/open-apis/bitable/v1/apps/:app_token/tables/:table_id/records
HTTP Method | POST
Rate Limit | [50 per second](https://open.feishu.cn/document/ukTMukTMukTM/uUzN04SN3QjL1cDN)
Supported app types | Custom App、Store App
Required scopes<br>**To use this API, you must have at least 1 of the listed scopes.**<br>Enable any scope from the list | 新增记录(base:record:create)<br>View, comment, edit and manage Base(bitable:app)
Required field scopes | **Notice**：The response body of the API contains the following sensitive fields, and they will be returned only after corresponding scopes are added. If you do not need the fields, it is not recommended that you request the scopes.<br>Obtain user's basic information(contact:user.base:readonly)<br>Obtain user ID(contact:user.employee_id:readonly)<br>Access Contacts as an app(contact:contact:access_as_app)<br>Read contacts(contact:contact:readonly)<br>Read Contacts as an app(contact:contact:readonly_as_app)

### Request header

Parameter | Type | Required | Description
---|---|---|---
Authorization | string | Yes | `tenant_access_token`<br>or<br>`user_access_token`<br>**Value format**: "Bearer `access_token`"<br>**Example value**: "Bearer u-7f1bcd13fc57d46bac21793a18e560"<br>[How to choose and get access token](https://open.feishu.cn/document/uAjLw4CM/ugTN1YjL4UTN24CO1UjN/trouble-shooting/how-to-choose-which-type-of-token-to-use)
Content-Type | string | Yes | **Fixed value**: "application/json; charset=utf-8"

### Path parameters

Parameter | Type | Description
---|---|---
app_token | string | Base unique device identifier [app_token description](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/bitable/notification#8121eebe)<br>**Example value**: "appbcbWCzen6D8dezhoCH2RpMAh"
table_id | string | Base data table unique device identifier [table_id description](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/bitable/notification#735fe883)<br>**Example value**: "tblsRc9GRRXKqhvW"

### Query parameters

Parameter | Type | Required | Description
---|---|---|---
user_id_type | string | No | User ID categories<br>**Example value**: open_id<br>**Optional values are**:<br>- open_id：Identifies a user to an app. The same user has different Open IDs in different apps. [How to get Open ID](https://open.feishu.cn/document/uAjLw4CM/ugTN1YjL4UTN24CO1UjN/trouble-shooting/how-to-obtain-openid)<br>- union_id：Identifies a user to a tenant that acts as a developer. A user has the same Union ID in apps developed by the same developer, and has different Union IDs in apps developed by different developers. A developer can use Union ID to link the same user's identities in multiple apps.[How to get Union ID](https://open.feishu.cn/document/uAjLw4CM/ugTN1YjL4UTN24CO1UjN/trouble-shooting/how-to-obtain-union-id)<br>- user_id：Identifies a user to a tenant. The same user has different User IDs in different tenants. In one single tenant, a user has the same User ID in all apps （including store apps）. User ID is usually used to communicate user data between different apps. [How to get User ID](https://open.feishu.cn/document/uAjLw4CM/ugTN1YjL4UTN24CO1UjN/trouble-shooting/how-to-obtain-user-id)<br>**Default value**: `open_id`<br>**When the value is `user_id`, the following field scopes are required**:<br>Obtain user ID(contact:user.employee_id:readonly)
client_token | string | No | The format is a standard uuidv4, the unique identifier of the operation, used for idempotent update operations. This value is null to indicate that a new request will be initiated, and this value is non-null to indicate idempotent update operations.<br>**Example value**: fe599b60-450f-46ff-b2ef-9f6675625b97
ignore_consistency_check | boolean | No | Whether to ignore consistency checks for read and write operations. The default value is `false`, meaning the system will ensure that the data read and written is consistent. Optional values:<br>- **true**: Ignore read/write consistency checks to improve performance, but this may cause data on some nodes to be out of sync, resulting in temporary inconsistency.<br>- **false**: Enable read/write consistency checks to ensure data consistency during read and write operations.<br>**Example value**: true

### Request body

Parameter | Type | Required | Description
---|---|---|---
fields | map&lt;string, union&gt; | Yes | To add new records to the data table, you need to first specify the fields in the table (i.e., specify the columns) and then pass the correctly formatted data as a record.<br>**Note**:<br>The supported field types and their descriptions are as follows:<br>- Text: Enter a value in string format<br>- Number: Enter a value in number format<br>- Single choice: Enter an option value; for new option values, a new option will be created<br>- Multiple choices: Enter multiple option values; for new option values, multiple new options will be created if multiple identical new option values are entered<br>- Date: Enter a timestamp in milliseconds<br>- Checkbox: Enter true or false<br>- Barcode<br>- Person: Enter the user's [open_id](https://open.feishu.cn/document/uAjLw4CM/ugTN1YjL4UTN24CO1UjN/trouble-shooting/how-to-obtain-openid), [union_id](https://open.feishu.cn/document/uAjLw4CM/ugTN1YjL4UTN24CO1UjN/trouble-shooting/how-to-obtain-union-id) or [user_id](https://open.feishu.cn/document/uAjLw4CM/ugTN1YjL4UTN24CO1UjN/trouble-shooting/how-to-obtain-user-id); the type must match the type specified by user_id_type<br>- Phone number: Enter text content<br>- Hyperlink: Refer to the following example, text is the text value, link is the URL link<br>- Attachment: Enter the attachment token; you need to first call the [upload material](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/drive-v1/media/upload_all) or [fragmented upload material](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/drive-v1/media/upload_prepare) interface to upload the attachment to this Base<br>- One-way association: Enter the record ID of the associated table<br>- Two-way association: Enter the record ID of the associated table<br>- Location: Enter the latitude and longitude coordinates<br>For the data structure of different types of fields, please refer to the [Base record data structure overview](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/bitable-v1/app-table-record/bitable-record-data-structure-overview).<br>**Example value**: {"multiline":"HelloWorld"}

### Request body example
```json
{
  "fields": {
    "text": "text",
    "barcode": "+$$3170930509104X512356",
    "number": 100,
    "currency": 3,
    "rating": 3,
    "progress": 0.25,
    "single_select": "option_1",
    "multi_select": [
      "option_1",
      "option_2"
    ],
    "date": 1674206443000,
    "checkbox": true,
    "user": [
      {
        "id": "ou_2910013f1e6456f16a0ce75ede950a0a"
      },
      {
        "id": "ou_e04138c9633dd0d2ea166d79f548ab5d"
      }
    ],
    "GroupChat": [
      {
        "id": "oc_cd07f55f14d6f4a4f1b51504e7e97f48"
      }
    ],
    "phone": "13026162666",
    "url": {
      "text": "Base",
      "link": "https://www.feishu.cn/product/base"
    },
    "attachment": [
      {
        "file_token": "DRiFbwaKsoZaLax4WKZbEGCccoe"
      },
      {
        "file_token": "BZk3bL1Enoy4pzxaPL9bNeKqcLe"
      },
      {
        "file_token": "EmL4bhjFFovrt9xZgaSbjJk9c1b"
      },
      {
        "file_token": "Vl3FbVkvnowlgpxpqsAbBrtFcrd"
      }
    ],
    "single_link": [
      "recHTLvO7x",
      "recbS8zb2m"
    ],
    "duplex_link": [
      "recHTLvO7x",
      "recbS8zb2m"
    ],
    "location": "116.397755,39.903179"
  }
}
```

## Response

### Response body

Parameter | Type | Description
---|---|---
code | int | Error codes, fail if not zero
msg | string | Error descriptions
data | \- | \-
record | app.table.record | records
fields | map&lt;string, union&gt; | fields
record_id | string | record id，Update records are required
created_by | person | record creator
id | string | user id
name | string | user name
en_name | string | user english name
email | string | user email
avatar_url | string | user avatar url<br>**Required field scopes (Satisfy any)**:<br>Obtain user's basic information(contact:user.base:readonly)<br>Access Contacts as an app(contact:contact:access_as_app)<br>Read contacts(contact:contact:readonly)<br>Read Contacts as an app(contact:contact:readonly_as_app)
created_time | int | record create timestamp
last_modified_by | person | the person who last modified the record
id | string | user id
name | string | user name
en_name | string | user english name
email | string | user email
avatar_url | string | user avatar url<br>**Required field scopes (Satisfy any)**:<br>Obtain user's basic information(contact:user.base:readonly)<br>Access Contacts as an app(contact:contact:access_as_app)<br>Read contacts(contact:contact:readonly)<br>Read Contacts as an app(contact:contact:readonly_as_app)
last_modified_time | int | record last modified timestamp
shared_url | string | Record sharing link (the batch fetch records interface will return this field)
record_url | string | Record link (the retrieve record interface will return this field)

### Response body example
```json
{
	"code": 0,
	"data": {
		"record": {
			"fields": {
				"text": "text",
                "barcode": "+$$3170930509104X512356",
				"number": 100,
                "currency":3,
                "rating":3,
                "progress":0.25,
				"single_select": "option_1",
				"multi_select": ["option_1", "option_2"],
				"date": 1674206443000,
				"checkbox": true,
				"user": [{
					"id": "ou_2910013f1e6456f16a0ce75ede950a0a"
				}, {
					"id": "ou_e04138c9633dd0d2ea166d79f548ab5d"
				}],
                "GroupChat": [
                    {
                        "id": "oc_cd07f55f14d6f4a4f1b51504e7e97f48"
                    }
                ],
				"phone": "13026162666",
				"url": {
					"text": "Base",
					"link": "https://www.feishu.cn/product/base"
				},
				"attachment": [{
					"file_token": "DRiFbwaKsoZaLax4WKZbEGCccoe"
				}, {
					"file_token": "BZk3bL1Enoy4pzxaPL9bNeKqcLe"
				}, {
					"file_token": "EmL4bhjFFovrt9xZgaSbjJk9c1b"
				}, {
					"file_token": "Vl3FbVkvnowlgpxpqsAbBrtFcrd"
				}],
				"single_link": ["recHTLvO7x", "recbS8zb2m"],
				"duplex_link": ["recHTLvO7x", "recbS8zb2m"],
				"location": "116.397755,39.903179"
			},
			"id": "reclAqylTN",
			"record_id": "reclAqylTN"
		}
	},
	"msg": "success"
}
```

### Error code

HTTP status code | Error code | Description | Troubleshooting suggestions
---|---|---|---
200 | 1254000 | WrongRequestJson | Request error
200 | 1254001 | WrongRequestBody | Request body error
200 | 1254002 | Fail | Internal error, have any questions can be consulting service
200 | 1254003 | WrongBaseToken | AppToken error
200 | 1254004 | WrongTableId | Table id wrong
200 | 1254005 | WrongViewId | View id wrong
200 | 1254006 | WrongRecordId | Record id wrong
200 | 1254007 | EmptyValue | Empty value
200 | 1254008 | EmptyView | Empty view
200 | 1254009 | WrongFieldId | Wrong fieldId
200 | 1254010 | ReqConvError | Request error
400 | 1254015 | Field types do not match. | FieldTypeValueNotMatch
403 | 1254027 | UploadAttachNotAllowed | Attachments don't belong to the app, not allowed to upload
200 | 1254030 | TooLargeResponse | TooLargeResponse
400 | 1254036 | Base is copying, please try again later. | Base copy replicating, try again later
400 | 1254037 | Invalid client token, make sure that it complies with the specification. | Idempotent key format is wrong, you need to pass in uuidv4 format
200 | 1254040 | BaseTokenNotFound | AppToken not found
200 | 1254041 | TableIdNotFound | Table not found
200 | 1254042 | ViewIdNotFound | View not found
200 | 1254043 | RecordIdNotFound | RecordIdNotFound
200 | 1254044 | FieldIdNotFound | FieldIdNotFound
200 | 1254045 | FieldNameNotFound | Field name does not exist
200 | 1254060 | TextFieldConvFail | TextFieldConvFail
200 | 1254061 | NumberFieldConvFail | NumberFieldConvFail
200 | 1254062 | SingleSelectFieldConvFail | SingleSelectFieldConvFail
200 | 1254063 | MultiSelectFieldConvFail | MultiSelectFieldConvFail
200 | 1254064 | DatetimeFieldConvFail | DatetimeFieldConvFail
200 | 1254065 | CheckboxFieldConvFail | CheckboxFieldConvFail
200 | 1254066 | UserFieldConvFail | The value corresponding to the personnel field type is incorrect. The possible reasons are:<br>- The ID type specified by the user_id_type parameter does not match the type of the provided ID.<br>- An unrecognized type or structure was provided. Currently, only `id` is supported, and it must be passed as an array.<br>- An `open_id` was passed across applications. If you are passing an ID across applications, it is recommended to use `user_id`. The `open_id` obtained from different applications cannot be used interchangeably.
200 | 1254067 | LinkFieldConvFail | LinkFieldConvFail
200 | 1254068 | URLFieldConvFail | URLFieldConvFail
200 | 1254069 | AttachFieldConvFail | AttachFieldConvFail
200 | 1254072 | Failed to convert phone field, please make sure it is correct. | Phone field error
400 | 1254074 | The parameters of Duplex Link field are invalid and need to be filled with an array of string. | DuplexLinkFieldConvFail
200 | 1254100 | TableExceedLimit | TableExceedLimit, limited to 300
200 | 1254101 | ViewExceedLimit | ViewExceedLimit, limited to 200
200 | 1254102 | FileExceedLimit | FileExceedLimit
200 | 1254103 | RecordExceedLimit | RecordExceedLimit, limited to 20,000
200 | 1254104 | RecordAddOnceExceedLimit | RecordAddOnceExceedLimit, limited to 500
200 | 1254105 | ColumnExceedLimit | ColumnExceedLimit
200 | 1254106 | AttachExceedLimit | AttachExceedLimit
200 | 1254130 | TooLargeCell | TooLargeCell
200 | 1254290 | TooManyRequest | Request too fast, try again later
200 | 1254291 | Write conflict | The same data table does not support concurrent calls to the write interface, please check whether there is a concurrent call to the write interface. The writing interface includes: adding, modifying, and deleting records; adding, modifying, and deleting fields; modifying forms; modifying views, etc.
200 | 1254301 | OperationTypeError | Base does not have advanced permissions enabled or does not support enabling advanced permissions
200 | 1254303 | The attachment does not belong to this base. | No attach permission
200 | 1255001 | InternalError | Internal error, have any questions can be consulting service
200 | 1255002 | RpcError | Internal error, have any questions can be consulting service
200 | 1255003 | MarshalError | Serialization failed, have any questions can be consulting service
200 | 1255004 | UmMarshalError | Deserialization failed, have any questions can be consulting service
200 | 1255005 | ConvError | Internal error, have any questions can be consulting service
400 | 1255006 | Client token conflict, please generate a new client token and try again. | Idempotent key conflict, you need to randomly generate an idempotent key
504 | 1255040 | Request timed out, please try again later | Try again
400 | 1254607 | Data not ready, please try again later | There are usually two situations when this error occurs: 1. The last submitted modification has not been processed; 2. The data is too large and the server calculation times out; <br>This error code can be appropriately retried.
403 | 1254302 | Permission denied. | No access rights, usually caused by the table opening of advanced permissions, please add a group containing applications in the advanced permissions settings and give this group read and write permissions
403 | 1254304 | Permission denied. | Advanced permissions for specific rows or columns are only available for Business and Enterprise editions
403 | 1254306 | The tenant or base owner is subject to base plan limits. | The tenant or base owner is subject to base plan limits.
403 | 1254608 | Same API requests are submitted repeatedly. | Same API requests are submitted repeatedly.
