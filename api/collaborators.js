/* Live collaborators and invited members avatar grid for the README.
 *
 *   GET /api/collaborators/  ->  image/svg+xml   (trailing slash: vercel.json sets trailingSlash)
 *   GET /api/members/        ->  image/svg+xml
 *
 * Gathers repository collaborators (accepted) and pending invitations from GitHub REST API,
 * so both accepted collaborators and newly invited members appear in one 12-column circular avatar grid.
 * Updates dynamically on invite without needing a commit or workflow.
 * Avatars are embedded as data URIs because an SVG shown as an <img> cannot load external images.
 */
'use strict';

const REPO = 'JayDev-27/Frontend-Library';
const SIZE = 64;
const GAP = 8;
const COLUMNS = 12;

const FALLBACK_MEMBERS = [
  { login: 'satiricalguru', status: 'collaborator', avatar_url: 'https://avatars.githubusercontent.com/u/227462757?v=4', is_owner: true },
  { login: 'auroraeye-dev', status: 'collaborator', avatar_url: 'https://avatars.githubusercontent.com/u/191999359?v=4' },
  { login: 'eshikaatreya', status: 'collaborator', avatar_url: 'https://avatars.githubusercontent.com/u/317296881?v=4' },
  { login: 'JayDev-27', status: 'collaborator', avatar_url: 'https://avatars.githubusercontent.com/u/279688498?v=4' },
  { login: 'Mxhi-04', status: 'collaborator', avatar_url: 'https://avatars.githubusercontent.com/u/249584456?v=4' },
  { login: 'Phantom-lj', status: 'collaborator', avatar_url: 'https://avatars.githubusercontent.com/u/86778112?v=4' },
  { login: 'pratejash', status: 'collaborator', avatar_url: 'https://avatars.githubusercontent.com/u/320674383?v=4' },
  { login: 'Rashmi-builds', status: 'collaborator', avatar_url: 'https://avatars.githubusercontent.com/u/317297793?v=4' },
  { login: 'Vedant275', status: 'collaborator', avatar_url: 'https://avatars.githubusercontent.com/u/218742536?v=4' },
  { login: 'Aaravcodesss', status: 'invited', avatar_url: 'https://avatars.githubusercontent.com/u/212439928?v=4' },
  { login: 'arsh-WINsingh', status: 'invited', avatar_url: 'https://avatars.githubusercontent.com/u/275754707?v=4' },
  { login: 'ChetasLua', status: 'invited', avatar_url: 'https://avatars.githubusercontent.com/u/140589714?v=4' },
  { login: 'jasroopbhinder', status: 'invited', avatar_url: 'https://avatars.githubusercontent.com/u/305776386?v=4' },
  { login: 'jassi-mocking-it', status: 'invited', avatar_url: 'https://avatars.githubusercontent.com/u/259535430?v=4' },
  { login: 'nullprsn', status: 'invited', avatar_url: 'https://avatars.githubusercontent.com/u/78124544?v=4' },
  { login: 'pedroiff0', status: 'invited', avatar_url: 'https://avatars.githubusercontent.com/u/137837852?v=4' },
  { login: 'prabhakarkavyansh', status: 'invited', avatar_url: 'https://avatars.githubusercontent.com/u/318371832?v=4' },
  { login: 'ravindrasinghp933-blip', status: 'invited', avatar_url: 'https://avatars.githubusercontent.com/u/343925505?v=4' },
  { login: 'Saket-code40', status: 'invited', avatar_url: 'https://avatars.githubusercontent.com/u/185668607?v=4' },
  { login: 'yashadityaixd7544-oss', status: 'invited', avatar_url: 'https://avatars.githubusercontent.com/u/244797493?v=4' },
];

const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&apos;' }[c]));

const avatarCache = new Map();

async function gh(path) {
  const headers = { Accept: 'application/vnd.github+json', 'User-Agent': 'Frontend-Library-Collaborators' };
  const token = process.env.GITHUB_TOKEN || process.env.GH_TOKEN;
  if (token) headers.Authorization = `Bearer ${token}`;
  const r = await fetch(`https://api.github.com${path}`, { headers });
  if (r.status === 404) return null;
  if (!r.ok) throw new Error(`GitHub ${r.status} for ${path}`);
  return r.json();
}

async function dataUri(url) {
  if (!url) return null;
  const key = `${url}${url.includes('?') ? '&' : '?'}s=96`;
  if (avatarCache.has(key)) return avatarCache.get(key);
  const r = await fetch(key);
  if (!r.ok) throw new Error(`avatar ${r.status}`);
  const type = (r.headers.get('content-type') || 'image/png').split(';')[0];
  const uri = `data:${type.startsWith('image/') ? type : 'image/png'};base64,${Buffer.from(await r.arrayBuffer()).toString('base64')}`;
  avatarCache.set(key, uri);
  return uri;
}

async function gather() {
  const people = new Map();
  const owner = 'JayDev-27'.toLowerCase();

  try {
    const collabs = (await gh(`/repos/${REPO}/collaborators?per_page=100`)) || [];
    for (const c of collabs) {
      if (!c?.login) continue;
      people.set(c.login.toLowerCase(), {
        login: c.login,
        avatar: c.avatar_url,
        status: 'collaborator',
        isOwner: c.login.toLowerCase() === owner,
      });
    }
  } catch (err) {
    // Falls back gracefully if token is absent or API fails
  }

  try {
    const invites = (await gh(`/repos/${REPO}/invitations?per_page=100`)) || [];
    for (const inv of invites) {
      const invitee = inv?.invitee;
      if (!invitee?.login) continue;
      const key = invitee.login.toLowerCase();
      if (!people.has(key)) {
        people.set(key, {
          login: invitee.login,
          avatar: invitee.avatar_url,
          status: 'invited',
          isOwner: false,
        });
      }
    }
  } catch (err) {
    // Falls back gracefully if token is absent or API fails
  }

  // Fallback to offline/snapshot members if GitHub API was unreachable or unauthenticated
  if (people.size === 0) {
    for (const f of FALLBACK_MEMBERS) {
      people.set(f.login.toLowerCase(), {
        login: f.login,
        avatar: f.avatar_url,
        status: f.status,
        isOwner: Boolean(f.is_owner),
      });
    }
  } else if (!people.has(owner)) {
    people.set(owner, {
      login: 'satiricalguru',
      avatar: 'https://avatars.githubusercontent.com/u/227462757?v=4',
      status: 'collaborator',
      isOwner: true,
    });
  }

  const list = [...people.values()].sort((a, b) => {
    if (a.isOwner) return -1;
    if (b.isOwner) return 1;
    if (a.status !== b.status) {
      return a.status === 'collaborator' ? -1 : 1;
    }
    return a.login.localeCompare(b.login, undefined, { sensitivity: 'base' });
  });

  await Promise.all(
    list.map(async (p) => {
      try {
        p.uri = await dataUri(p.avatar);
      } catch {
        p.uri = null;
      }
    })
  );

  return list;
}

function render(items) {
  const cols = Math.min(COLUMNS, Math.max(1, items.length));
  const rows = Math.max(1, Math.ceil(items.length / COLUMNS));
  const w = cols * SIZE + (cols - 1) * GAP;
  const h = rows * SIZE + (rows - 1) * GAP;
  const r = SIZE / 2 - 1;
  const defs = [];
  const nodes = [];

  items.forEach((p, i) => {
    const x = (i % COLUMNS) * (SIZE + GAP);
    const y = Math.floor(i / COLUMNS) * (SIZE + GAP);
    const roleLabel = p.isOwner ? 'Owner' : p.status === 'invited' ? 'Invited Member' : 'Collaborator';
    const label = `${p.login} (${roleLabel})`;
    defs.push(`<clipPath id="c${i}"><circle cx="${SIZE / 2}" cy="${SIZE / 2}" r="${r}"/></clipPath>`);
    nodes.push(
      `<g transform="translate(${x},${y})"><title>${esc(label)}</title>` +
        `<circle cx="${SIZE / 2}" cy="${SIZE / 2}" r="${r}" fill="#0d1117"/>` +
        (p.uri
          ? `<image x="1" y="1" width="${SIZE - 2}" height="${SIZE - 2}" href="${p.uri}" xlink:href="${p.uri}" clip-path="url(#c${i})" preserveAspectRatio="xMidYMid slice"/>`
          : `<text x="${SIZE / 2}" y="${SIZE / 2 + 7}" text-anchor="middle" font-family="Arial,sans-serif" font-size="20" fill="#d0d7de">${esc(p.login.slice(0, 2).toUpperCase())}</text>`) +
        `<circle cx="${SIZE / 2}" cy="${SIZE / 2}" r="${r}" fill="none" stroke="#d0d7de" stroke-opacity="0.7" stroke-width="1.5"/></g>`
    );
  });

  const title = `Frontend Library collaborators and invited members (${items.length})`;
  return `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" role="img" aria-label="${esc(title)}"><title>${esc(title)}</title><defs>${defs.join('')}</defs>${nodes.join('')}</svg>`;
}

module.exports = async (req, res) => {
  try {
    const svg = render(await gather());
    res.setHeader('Content-Type', 'image/svg+xml; charset=utf-8');
    // Cache briefly (1 min) so newly sent invites and accepted collaborators appear without delay
    res.setHeader('Cache-Control', 'public, max-age=60, s-maxage=60, stale-while-revalidate=300');
    res.status(200).send(svg);
  } catch (err) {
    res.status(500).send(`<!-- error: ${esc(err.message)} -->`);
  }
};
