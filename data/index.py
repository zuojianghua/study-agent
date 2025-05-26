import os
import asyncio
from lightrag import LightRAG, QueryParam
from lightrag.llm.openai import openai_complete_if_cache
from lightrag.llm.siliconcloud import siliconcloud_embedding
# from lightrag.llm.ollama import ollama_complete
from lightrag.kg.shared_storage import initialize_pipeline_status
from lightrag.utils import setup_logger, EmbeddingFunc
import numpy as np


from dotenv import load_dotenv
load_dotenv("../.env", override=True)

setup_logger("lightrag", level="INFO")

WORKING_DIR = "./rag_storage_yw"
if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)


async def llm_model_func(
    prompt, system_prompt=None, history_messages=[], keyword_extraction=False, **kwargs
) -> str:
    return await openai_complete_if_cache(
        os.getenv("LLM_MODEL_NAME"),
        prompt,
        system_prompt=system_prompt,
        history_messages=history_messages,
        api_key=os.getenv("LLM_API_KEY"),
        base_url=os.getenv("LLM_BASE_URL"),
        **kwargs,
    )

async def embedding_func(texts: list[str]) -> np.ndarray:
    return await siliconcloud_embedding(
        texts,
        model=os.getenv("EMBED_MODEL_NAME"),
        api_key=os.getenv("EMBED_API_KEY"),
        base_url=os.getenv("EMBED_BASE_URL"),
    )


async def get_embedding_dim():
    test_text = ["This is a test sentence."]
    embedding = await embedding_func(test_text)
    embedding_dim = embedding.shape[1]
    return embedding_dim


async def initialize_rag():
    embedding_dimension = await get_embedding_dim()
    rag = LightRAG(
        working_dir=WORKING_DIR,
        embedding_func=EmbeddingFunc(
            embedding_dim=embedding_dimension,
            max_token_size=8192,
            func=embedding_func,
        ),
        llm_model_func=llm_model_func,
        addon_params={"language": "Simplified Chinese"},
        chunk_token_size=1200,
        chunk_overlap_token_size=100,
        # llm_model_max_token_size=16384,
        max_parallel_insert = 1,
        enable_llm_cache=False,
    )
    await rag.initialize_storages()
    await initialize_pipeline_status()
    return rag

async def main():
    try:
        # Initialize RAG instance
        rag = await initialize_rag()

        file_path = "./yw_6_0/auto/yw_6_0.md"
        with open(file_path, 'r', encoding='utf-8') as f:
            txt=f.read()
            # print(txt)
        # await rag.ainsert(txt)

        # Perform hybrid search
        mode="mix"
        print(
            await rag.aquery(
                "请列出6年级上语文课文的各单元目录",
                param=QueryParam(mode=mode)
            )
        )

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if rag:
            await rag.finalize_storages()

if __name__ == "__main__":
    asyncio.run(main())