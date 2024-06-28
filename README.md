# BLAST-SummAIrizer

An easy-to-use, intuitive chat interface to ease and speed BLAST results interpretation, starting from 16S rRNA local blasting within the Docker container or from a Description Table (CSV) downloaded from online BLAST results.

## Run locally

1. Pull the Docker image:
   ```bash
   docker pull astrabert/blast-summaraizer:latest
   ```

2. Run the imagine:
   ```bash
   docker run -p 7860:7860 astrabert/blast-summaraizer:latest
   ```

3. The app will pop up on `http://localhost:7860` after 30-60 s.

## Use it online
### Hugging Face demo

Use directly the Hugging Face Space demo that you can find [here](https://huggingface.co/spaces/as-cle-bert/BLAST-SummarAIzer)

### Use GitHub CodeSpaces

Click the `Code<>` green button and then click on `CodeSpaces -> Create CodeSpace on 'main'`. 

You should be redirected to a VSCode-based space connected to the port on which the app runs, directly accessible under the "Ports" section of the VSCode interface.
