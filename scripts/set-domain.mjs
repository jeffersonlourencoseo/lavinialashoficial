// Roda no build da Vercel: troca o domínio de exemplo pelo domínio real em todos os arquivos de site/.
// Prioridade: variável SITE_URL na Vercel > site.config.json (domínio oficial do repositório) > domínio de produção da Vercel > URL do deploy.
import { readdirSync, readFileSync, writeFileSync, statSync } from "node:fs";
import { join, extname, resolve } from "node:path";

const PLACEHOLDER = "https://SITE_URL_PLACEHOLDER";
const root = resolve(process.argv[2] || "site");

const cfg = JSON.parse(readFileSync(resolve("site.config.json"), "utf8"));
let url = process.env.SITE_URL
  || cfg.siteUrl
  || (process.env.VERCEL_PROJECT_PRODUCTION_URL && "https://" + process.env.VERCEL_PROJECT_PRODUCTION_URL)
  || (process.env.VERCEL_URL && "https://" + process.env.VERCEL_URL);
if (!url) { console.error("Defina SITE_URL (ex.: https://www.seudominio.com.br)"); process.exit(1); }
url = url.replace(/\/+$/, "");
if (!/^https?:\/\//.test(url)) url = "https://" + url;

let files = 0, hits = 0;
(function walk(dir) {
  for (const name of readdirSync(dir)) {
    const p = join(dir, name);
    if (statSync(p).isDirectory()) { walk(p); continue; }
    if (![".html", ".xml", ".txt", ".json"].includes(extname(p))) continue;
    const t = readFileSync(p, "utf8");
    if (!t.includes(PLACEHOLDER)) continue;
    hits += t.split(PLACEHOLDER).length - 1;
    writeFileSync(p, t.split(PLACEHOLDER).join(url));
    files++;
  }
})(root);
console.log(`set-domain: ${url} -> ${hits} ocorrências em ${files} arquivos`);
