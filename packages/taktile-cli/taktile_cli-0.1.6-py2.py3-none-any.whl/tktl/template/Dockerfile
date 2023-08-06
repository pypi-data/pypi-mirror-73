FROM taktile/base-serving-api:34b0eb6731958390ebdc9636649e7d40f4a07c94
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
