# Use an official Python runtime as a parent image
FROM astrabert/blast-summaraizer

RUN cp -r /usr/local/ncbi-blast-2.15.0+/bin/* /usr/local/bin/

EXPOSE 7860

ENTRYPOINT [ "python3", "app.py" ]