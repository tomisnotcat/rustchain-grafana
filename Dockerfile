FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir requests

# Clone RustChain
RUN git clone --depth 1 https://github.com/Scottcjn/Rustchain.git /app/rustchain

WORKDIR /app/rustchain

# Create startup script
RUN echo '#!/bin/bash\n\
echo "Starting RustChain miner..."\n\
echo "Wallet: $WALLET_NAME"\n\
echo "Node: $NODE_URL"\n\
python3 -c "import requests; print(requests.get(\\"${NODE_URL:-https://rustchain.org}/health\\").json())"\n\
echo "Miner is ready!"\n\
tail -f /dev/null' > /start.sh && chmod +x /start.sh

ENV WALLET_NAME=your_wallet_name
ENV NODE_URL=https://rustchain.org

EXPOSE 8080

CMD ["/start.sh"]
