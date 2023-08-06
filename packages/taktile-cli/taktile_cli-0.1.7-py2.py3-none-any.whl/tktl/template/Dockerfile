FROM taktile/base-serving-api:ae59dc07b91413d11b71bb810b8ddadcf9b5f960
ENV APPDIR /app

# Install requirements
COPY ./requirements.txt ${APPDIR}/user_requirements.txt
RUN pip install -r ${APPDIR}/user_requirements.txt

# Copy code and assets for running the application
COPY ./src ${APPDIR}/src
COPY ./assets ${APPDIR}/assets
COPY ./tests ${APPDIR}/user_tests

# Run model profile
RUN python ${APPDIR}/profile_endpoints.py
