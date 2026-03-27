from data_pipeline.auto_ingest import ingest_pdf

ingest_pdf("data/constitution_of_india.pdf", "Constitution")
ingest_pdf("data/ipc.pdf", "IPC")