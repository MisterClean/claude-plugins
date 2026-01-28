/**
 * Chicago Data Portal query examples using TypeScript/JavaScript.
 * Works in Node.js, Deno, Bun, or browsers (with CORS).
 */

const BASE_URL = "https://data.cityofchicago.org/resource";
const METADATA_URL = "https://data.cityofchicago.org/api/views";

// Optional: Set via environment variable for higher rate limits
const APP_TOKEN = process.env.CHICAGO_DATA_PORTAL_TOKEN;

interface QueryParams {
  $select?: string;
  $where?: string;
  $group?: string;
  $having?: string;
  $order?: string;
  $limit?: number;
  $offset?: number;
}

interface ColumnMetadata {
  fieldName: string;
  dataTypeName: string;
  description: string;
}

/**
 * Query a Chicago dataset and return JSON results.
 */
async function queryDataset<T = Record<string, unknown>>(
  datasetId: string,
  params: QueryParams
): Promise<T[]> {
  const url = new URL(`${BASE_URL}/${datasetId}.json`);

  for (const [key, value] of Object.entries(params)) {
    if (value !== undefined) {
      url.searchParams.set(key, String(value));
    }
  }

  const headers: HeadersInit = {
    Accept: "application/json",
  };
  if (APP_TOKEN) {
    headers["X-App-Token"] = APP_TOKEN;
  }

  const response = await fetch(url.toString(), { headers });

  if (!response.ok) {
    throw new Error(`API error: ${response.status} ${response.statusText}`);
  }

  return response.json();
}

/**
 * Get dataset metadata including column definitions.
 */
async function getMetadata(datasetId: string): Promise<{
  name: string;
  description: string;
  rowsUpdatedAt: number;
  columns: ColumnMetadata[];
}> {
  const response = await fetch(`${METADATA_URL}/${datasetId}`);

  if (!response.ok) {
    throw new Error(`Metadata error: ${response.status}`);
  }

  return response.json();
}

/**
 * Paginate through large result sets.
 */
async function* paginateDataset<T = Record<string, unknown>>(
  datasetId: string,
  params: QueryParams,
  pageSize = 1000
): AsyncGenerator<T[], void, unknown> {
  let offset = 0;

  while (true) {
    const results = await queryDataset<T>(datasetId, {
      ...params,
      $limit: pageSize,
      $offset: offset,
    });

    if (results.length === 0) break;

    yield results;
    offset += pageSize;

    if (results.length < pageSize) break;
  }
}

// ============================================================
// Example Usage
// ============================================================

// Example 1: Recent crimes in a specific ward
async function getRecentCrimes() {
  const crimes = await queryDataset("ijzp-q8t2", {
    $select: "date, primary_type, description, block, latitude, longitude",
    $where: "date >= '2024-01-01' AND ward = '42'",
    $order: "date DESC",
    $limit: 100,
  });

  console.log(`Found ${crimes.length} crimes`);
  return crimes;
}

// Example 2: 311 requests aggregated by type
async function get311ByType() {
  const results = await queryDataset("v6vf-nfxy", {
    $select: "sr_type, count(*) as total",
    $where: "created_date >= '2024-01-01'",
    $group: "sr_type",
    $order: "total DESC",
    $limit: 20,
  });

  return results;
}

// Example 3: Geospatial - crimes near a location
async function getCrimesNearLocation(lat: number, lon: number, radiusMeters: number) {
  const crimes = await queryDataset("ijzp-q8t2", {
    $where: `within_circle(location, ${lat}, ${lon}, ${radiusMeters})`,
    $order: "date DESC",
    $limit: 100,
  });

  return crimes;
}

// Example 4: Get all pages of a large result set
async function getAllBuildingPermits2024() {
  const allPermits: Record<string, unknown>[] = [];

  for await (const page of paginateDataset("ydr8-5enu", {
    $where: "issue_date >= '2024-01-01'",
    $order: "issue_date DESC",
  })) {
    allPermits.push(...page);
    console.log(`Fetched ${allPermits.length} permits so far...`);
  }

  return allPermits;
}

// Example 5: Check column names before querying
async function inspectDataset(datasetId: string) {
  const meta = await getMetadata(datasetId);

  console.log(`Dataset: ${meta.name}`);
  console.log(`Description: ${meta.description}`);
  console.log(`Last updated: ${new Date(meta.rowsUpdatedAt * 1000).toISOString()}`);
  console.log("\nColumns:");

  for (const col of meta.columns) {
    console.log(`  ${col.fieldName} (${col.dataTypeName}): ${col.description || "No description"}`);
  }
}

// Run examples
async function main() {
  try {
    // Inspect the crimes dataset
    await inspectDataset("ijzp-q8t2");

    // Get recent crimes
    const crimes = await getRecentCrimes();
    console.log("\nRecent crimes sample:", crimes.slice(0, 3));

    // Get 311 by type
    const requests = await get311ByType();
    console.log("\n311 requests by type:", requests.slice(0, 5));

    // Geospatial query - crimes near Willis Tower
    const nearbycrimes = await getCrimesNearLocation(41.8789, -87.6359, 500);
    console.log(`\nCrimes within 500m of Willis Tower: ${nearbycrimes.length}`);
  } catch (error) {
    console.error("Error:", error);
  }
}

main();
