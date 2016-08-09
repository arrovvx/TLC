FROM arrovvx/tlc:env

# Create app directory
WORKDIR /src/

# Bundle app source
COPY . /src/

EXPOSE 8890
CMD [ "python", "TLC.py" ]