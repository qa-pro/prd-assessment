#!/usr/bin/env python3
"""
PRD 评分提交脚本
将 PRD 评估结果通过 HTTP POST 请求提交到后端数据库
"""

import sys
import json
import urllib.request
import urllib.error


def submit_prd_score(
    prd_doc_name: str,
    prd_link: str,
    submitter: str,
    business_line: str,
    product_score: float,
    backend_score: float,
    frontend_score: float,
    qa_score: float,
    design_score: float,
    global_score: float,
    global_level: str,
) -> bool:
    """
    提交 PRD 评分到后端接口

    Args:
        prd_doc_name: PRD 文档名称
        prd_link: PRD 文档链接
        submitter: 提交人
        business_line: 业务线（如：国际销售客户、国际销售合同等）
        product_score: 产品视角得分
        backend_score: 后端视角得分
        frontend_score: 前端视角得分
        qa_score: 测试/QA视角得分
        design_score: 设计视角得分
        global_score: 总分
        global_level: 等级

    Returns:
        bool: 提交是否成功
    """
    url = "http://10.38.219.120:80/fullstack/api/prd/score/submit"

    data = {
        "prdDocName": prd_doc_name,
        "prdLink": prd_link,
        "submitter": submitter,
        "businessLine": business_line,
        "productScore": product_score,
        "backendScore": backend_score,
        "frontendScore": frontend_score,
        "qaScore": qa_score,
        "designScore": design_score,
        "globalScore": global_score,
        "globalLevel": global_level,
    }
    
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                print(f"[INFO] PRD 评分提交成功: {prd_doc_name}")
                return True
            else:
                print(f"[WARN] PRD 评分提交失败，状态码: {response.status}")
                return False
                
    except urllib.error.URLError as e:
        print(f"[WARN] PRD 评分提交失败，网络错误: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"[WARN] PRD 评分提交失败，JSON 编码错误: {e}")
        return False
    except Exception as e:
        print(f"[WARN] PRD 评分提交失败，未知错误: {e}")
        return False


def main():
    """
    主函数：从命令行参数或标准输入读取评分数据并提交
    """
    if len(sys.argv) == 12:
        # 从命令行参数读取（脚本名 + 11个参数）
        prd_doc_name = sys.argv[1]
        prd_link = sys.argv[2]
        submitter = sys.argv[3]
        business_line = sys.argv[4]
        product_score = float(sys.argv[5])
        backend_score = float(sys.argv[6])
        frontend_score = float(sys.argv[7])
        qa_score = float(sys.argv[8])
        design_score = float(sys.argv[9])
        global_score = float(sys.argv[10])
        global_level = sys.argv[11]
    else:
        # 从标准输入读取 JSON
        try:
            data = json.load(sys.stdin)
            prd_doc_name = data["prdDocName"]
            prd_link = data["prdLink"]
            submitter = data["submitter"]
            business_line = data["businessLine"]
            product_score = float(data["productScore"])
            backend_score = float(data["backendScore"])
            frontend_score = float(data["frontendScore"])
            qa_score = float(data["qaScore"])
            design_score = float(data["designScore"])
            global_score = float(data["globalScore"]) if "globalScore" in data else 0.0
            global_level = data["globalLevel"] if "globalLevel" in data else ""
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"[ERROR] 无效的输入格式: {e}", file=sys.stderr)
            print("用法1: python3 submit_prd_score.py <prdDocName> <prdLink> <submitter> <businessLine> <productScore> <backendScore> <frontendScore> <qaScore> <designScore> <globalScore> <globalLevel>")
            print("用法2: echo '{\"prdDocName\": \"...\", \"businessLine\": \"...\", ...}' | python3 submit_prd_score.py")
            sys.exit(1)
    
    success = submit_prd_score(
        prd_doc_name,
        prd_link,
        submitter,
        business_line,
        product_score,
        backend_score,
        frontend_score,
        qa_score,
        design_score,
        global_score,
        global_level,
    )
    
    # 静默失败：即使提交失败也不退出码，不影响主流程
    sys.exit(0)


if __name__ == "__main__":
    main()
