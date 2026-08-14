const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;
const API_URL = process.env.API_URL || 'http://backend-api:8000';

app.use(express.static(path.join(__dirname, 'public')));

app.get('/health', (req, res) => {
  res.json({ status: 'healthy', service: 'frontend-web', timestamp: new Date().toISOString() });
});

app.get('/api/config', (req, res) => {
  res.json({ apiUrl: API_URL, version: process.env.APP_VERSION || '1.0.0' });
});

if (require.main === module) {
  app.listen(PORT, () => {
    console.log(`Frontend running on http://0.0.0.0:${PORT}`);
  });
}

module.exports = app;
