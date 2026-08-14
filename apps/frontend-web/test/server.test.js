const test = require('node:test');
const assert = require('node:assert');
const app = require('../server');
const http = require('http');

test('GET /health returns status healthy', async (t) => {
  const server = http.createServer(app);
  await new Promise((resolve) => server.listen(0, resolve));
  const port = server.address().port;

  const res = await fetch(`http://localhost:${port}/health`);
  const data = await res.json();

  assert.strictEqual(res.status, 200);
  assert.strictEqual(data.status, 'healthy');
  assert.strictEqual(data.service, 'frontend-web');

  await new Promise((resolve) => server.close(resolve));
});
