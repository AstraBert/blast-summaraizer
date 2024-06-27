import gradio as gr
from gradio_client import Client
import subprocess as sp
import time
import requests

def upload_to_fileio(file_path):
    with open(file_path, 'rb') as f:
        response = requests.post('https://file.io', files={'file': f})
    if response.status_code == 200:
        return response.json().get('link')
    else:
        return "#"

api_client = Client("eswardivi/Phi-3-mini-128k-instruct")

def blast_search(inputfile, matchesnumber, qcovcutoff, evaluecutoff):
    sp.run("echo 'QUERY_SEQ\tTAXON\tQUERY_COVERAGE\tPERC_ID\tLENGTH\tMISMATCHES\tGAPS\tE_VALUE\tBITSCORE' > results.txt", shell=True)
    sp.run(f"blastn -query {inputfile} -db 16S_ribosomal_RNA -outfmt '6 qseqid sscinames qcov pident length mismatch gapopen evalue bitscore' -max_target_seqs {matchesnumber} -evalue {evaluecutoff} -qcov_hsp_perc {qcovcutoff} >> results.txt", shell=True)
    f = open("results.txt")
    content = f.read()
    f.close()
    link = upload_to_fileio("results.txt")
    return content, link

def reply(user_prompt, history, inputfile, matchesnumber, qcovcutoff, evaluecutoff):
    context, filelink = blast_search(inputfile, matchesnumber, qcovcutoff, evaluecutoff)
    instructions = "You are a helpful assistant whose job is to summarize in a straight-to-the-point but effective way the result of a BLAST search conducted on a 16S rRNA bacterial sequences database from NCBI."
    full_prompt = f"{instructions} Based on thr content of this TSV file resulting from a BLAST search: \"\"\"{context}\"\"\", summarize the mentioned output complying with these user-provided instructions: {user_prompt}"
    response = api_client.predict(
        full_prompt,	# str  in 'Message' Textbox component
        0.2,	# float (numeric value between 0 and 1) in 'Temperature' Slider component
        True,	# bool  in 'Sampling' Checkbox component
        512,	# float (numeric value between 128 and 4096) in 'Max new tokens' Slider component
        api_name="/chat"
    )
    response = response + f"\n\nDownload you BLAST results [at this link]({filelink})"
    this_hist = ''
    for char in response:
        this_hist += char
        time.sleep(0.0001)
        yield this_hist

def summarize_description_table(description_table_file):
    f = open(description_table_file)
    lines = f.readlines()
    if len(lines) > 10:
        incipit = "**⚠️: The number of hits was higher than 10. Only the first 10 hits were taken into account.**\n\n"
        lines = lines[:11]
    else:
        incipit = ""
    content = "".join(lines)
    return incipit, content

def ai_summarize(user_prompt, history, inputfile):
    incipit, context = summarize_description_table(inputfile)
    instructions = "You are a helpful assistant whose job is to summarize in a straight-to-the-point but effective way the result of a BLAST search conducted online on NCBI databases."
    full_prompt = f"{instructions} Based on thr content of this CSV file resulting from a BLAST search: \"\"\"{context}\"\"\", summarize the mentioned output complying with these user-provided instructions: {user_prompt}"
    response = api_client.predict(
        full_prompt,	# str  in 'Message' Textbox component
        0.2,	# float (numeric value between 0 and 1) in 'Temperature' Slider component
        True,	# bool  in 'Sampling' Checkbox component
        512,	# float (numeric value between 128 and 4096) in 'Max new tokens' Slider component
        api_name="/chat"
    )
    response = incipit+response
    this_hist = ''
    for char in response:
        this_hist += char
        time.sleep(0.0001)
        yield this_hist


user_file = gr.File(label="Upload FASTA File")

user_file1 = gr.File(label="Upload Description Table (CSV) Downloadable From Online BLAST Results")

user_max_matches = gr.Slider(5, 50, value=20, label="Max Hits per Sequence", info="Select maximum number of BLAST hits per sequence (higher number of hits will result in a longer latency)")

user_qcov = gr.Slider(0, 100, value=0, label="Minimum Query Coverage", info="Minimum query coverage for a hit to be considered")

user_evalue = gr.Textbox(label="E-value threshold",info="All the hits below the threshold will be considered",value="1e-10")

additional_accordion = gr.Accordion(label="Parameters to be set before you start chatting", open=True)

demo0 = gr.ChatInterface(fn=reply, additional_inputs=[user_file, user_max_matches, user_qcov, user_evalue], additional_inputs_accordion=additional_accordion, title="""<h2 align='center'>Bacteria 16S rRNA</h2>
    <h3 align='center'>BLAST 16S rRNA bacterial sequences and get a nice summary of the results with the power of AI!</h3>
    <h4 align='center'>Support this space with a ⭐ on <a href='https://github.com/AstraBert/BLAST-SummarAIzer'>GitHub</a></h4>""")

demo1 = gr.ChatInterface(fn=ai_summarize, additional_inputs=[user_file1], additional_inputs_accordion=additional_accordion, title="""<h2 align='center'>Online BLAST results</h2>
    <h3 align='center'>Upload a Description Table from Online BLAST results and get a nice summary with the power of AI!</h3>
    <h4 align='center'>Support this space with a ⭐ on <a href='https://github.com/AstraBert/BLAST-SummarAIzer'>GitHub</a></h4>""")

demo = gr.TabbedInterface([demo0, demo1], ["16S rRNA", "Online BLAST results"], title="BLAST SummarAIzer")

if __name__=="__main__":
    demo.launch(server_name="0.0.0.0", share=False)