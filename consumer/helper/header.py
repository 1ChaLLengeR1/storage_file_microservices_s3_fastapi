from consumer.data.response import ResponseData


def check_required_headers(request, required_headers) -> ResponseData:
    try:
        missing_headers = []
        data_header = []

        for header in required_headers:
            if not request.headers.get(header):
                missing_headers.append(header)

        if missing_headers:
            return ResponseData(
                is_valid=False,
                data={"error": f'Missing headers: {", ".join(missing_headers)}'},
                status_code=403
            )

        for header in required_headers:
            if header == "key_main":
                data_header.append({
                    "header": header,
                    "data": request.headers.get(header)
                })
            elif header == "key_create":
                data_header.append({
                    "header": header,
                    "data": request.headers.get(header)
                })
            elif header == "key_delete":
                data_header.append({
                    "header": header,
                    "data": request.headers.get(header)
                })

        return ResponseData(
            is_valid=True,
            data=data_header,
            status_code=200
        )

    except Exception as e:
        return ResponseData(
            is_valid=False,
            data=str(e),
            status_code=403
        )
