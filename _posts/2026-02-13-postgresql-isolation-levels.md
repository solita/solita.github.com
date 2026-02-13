---
layout: post
title: SQL Isolation Levels
author: hjhamala
excerpt: The concept of ACID regarding transactions is familiar to many programmers but SQL isolation levels are relatively unfamiliar. This blog explains those in detail with interactive simulator.
tags:
  - PostgreSQL
  - SQL
  - Isolation levels
---

The concept of ACID regarding transactions is familiar to many programmers. It stands for four properties associated with database transactions.

The first of these is Atomicity, which means that a transaction is always executed either completely or not at all.

Consistency means that a transaction cannot violate database integrity rules. A transaction takes the DB from one valid state to another. One of those are foreign key and primary key constraints. This prevents, for example, the existence of a row with a foreign key that references a non-existent primary key.

Durability ensures that the changes made by a committed transaction are permanent. This is usually implemented with a separate transaction log, which guarantees that the data persists even if the database system crashes after the transaction has been committed.

I saved Isolation for last because, based on my experience interviewing software developers, this is an area relatively unfamiliar to many.

Since the best cure for a lack of knowledge is information, this blog post explains what isolation levels are, specifically from the perspective of a PostgreSQL database. I have also created interactive simulators to go through different scenarios with different isolation levels.

# Isolation in Brief

Isolation defines how a transaction perceives other concurrent transactions during its execution. It represents a trade-off between database performance and the prevention of concurrency anomalies. A higher isolation level typically means that transactions may block each other’s progress or even lead to transaction failures to ensure data integrity.

To understand these levels, we must first take a brief detour into how PostgreSQL stores data using the MVCC (Multi-Version Concurrency Control) model.

# MVCC

In a PostgreSQL database, records—or more simply, rows—are versioned rather than overwritten. When data is modified, the database creates a new version of the row instead of replacing the old one.

This is managed using internal metadata fields, specifically Transaction IDs:

- _$xmin$_ Stores the ID of the transaction that inserted the row version
- _$xmax$_ Stores the ID of the transaction that deleted or updated it.

From a query perspective, this mechanism ensures that a row cannot "disappear" in the middle of a read operation; the database simply checks these IDs to determine which version of the row is visible to your specific transaction. Consequently, data being added by a parallel process won't disrupt an ongoing transaction. A new version remains invisible until the transaction that created it has officially committed.

Understanding this versioning is essential as we move forward to examine the different isolation levels, which we will review from weakest to strongest.

# Isolation level 1: Read Uncommitted (Dirty Read)

This one is simple: no sane database — PostgreSQL included — allows a transaction to read uncommitted data. PostgreSQL accepts READ UNCOMMITTED, but it behaves the same as READ COMMITTED.

# Isolation level 2: Read Committed

This is the most important level to understand, as it is the default setting in PostgreSQL.

At this level, each query within a transaction sees only the data committed at the moment the query begins. While this prevents "dirty reads," it allows for two specific anomalies:

Non-repeatable Read: If you read the same row twice within the same transaction, you might get different results if another transaction committed changes to that row in between your two queries.

Phantom Read: This occurs when a query (such as an aggregate or a range scan) returns a different set of rows on a second execution because another transaction committed an INSERT or DELETE in the meantime. A "phantom" row has appeared or disappeared.

Whether these anomalies are a problem depends entirely on your application logic. A typical risk is making a functional decision or a calculation based on data that changes before the transaction finishes.

While there are ways to solve these issues at this isolation level—such as using specific locking clauses—we will return to those at the very end of this post.

To better understand how this works in practice, you can use the following simulator to test how transactions behave when running side-by-side. Keep in mind how Postgresql uses Transaction IDs to check rows visibility in a transaction.

<style>
    .rc-demo {
        --tx-a: #3b82f6;
        --tx-a-bg: #eff6ff;
        --tx-a-border: #bfdbfe;
        --tx-b: #f59e0b;
        --tx-b-bg: #fffbeb;
        --tx-b-border: #fde68a;
        --tx-old: #6b7280;
        --result-ok: #16a34a;
        --result-ok-bg: #f0fdf4;
        --result-warn: #d97706;
        --result-warn-bg: #fffbeb;
        --committed: #16a34a;
        --uncommitted: #9ca3af;
        --dead-bg: #f9fafb;
        --rc-gray-50: #f9fafb;
        --rc-gray-100: #f3f4f6;
        --rc-gray-200: #e5e7eb;
        --rc-gray-300: #d1d5db;
        --rc-gray-400: #9ca3af;
        --rc-gray-500: #6b7280;
        --rc-gray-600: #4b5563;
        --rc-gray-700: #374151;
        --rc-gray-800: #1f2937;
        --rc-gray-900: #111827;
        --rc-radius: 8px;
        --rc-font-mono: 'SF Mono', 'Fira Code', 'Fira Mono', Menlo, Consolas, monospace;
        --rc-font-sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    .rc-demo {
        font-family: var(--rc-font-sans);
        color: var(--rc-gray-800);
        line-height: 1.6;
        max-width: 900px;
        margin: 2rem auto;
        padding: 1.5rem;
        border: 1px solid var(--rc-gray-200);
        border-radius: var(--rc-radius);
        background: #fff;
    }

    .rc-demo .rc-title {
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
        color: var(--rc-gray-900);
    }

    .rc-demo .subtitle {
        color: var(--rc-gray-500);
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }

    .rc-demo .tabs {
        display: flex;
        gap: 0.25rem;
        border-bottom: 2px solid var(--rc-gray-200);
        margin-bottom: 1.5rem;
        overflow-x: auto;
    }

    .rc-demo .tab {
        padding: 0.6rem 1rem;
        border: none;
        background: none;
        font-family: var(--rc-font-sans);
        font-size: 0.875rem;
        font-weight: 500;
        color: var(--rc-gray-500);
        cursor: pointer;
        border-bottom: 2px solid transparent;
        margin-bottom: -2px;
        white-space: nowrap;
        transition: color 0.15s, border-color 0.15s;
    }

    .rc-demo .tab:hover { color: var(--rc-gray-700); }
    .rc-demo .tab.active { color: var(--tx-a); border-bottom-color: var(--tx-a); }

    .rc-demo .timelines {
        display: flex;
        gap: 1.5rem;
        margin-bottom: 1.5rem;
    }

    .rc-demo .timeline { flex: 1; min-width: 0; }

    .rc-demo .timeline-header {
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        padding: 0.4rem 0.75rem;
        border-radius: var(--rc-radius) var(--rc-radius) 0 0;
        margin-bottom: 0;
    }

    .rc-demo .timeline-header .txid {
        font-weight: 400; opacity: 0.7; font-size: 0.75rem;
        text-transform: none; letter-spacing: 0;
    }

    .rc-demo .timeline-header.tx-a {
        color: var(--tx-a); background: var(--tx-a-bg);
        border: 1px solid var(--tx-a-border); border-bottom: none;
    }

    .rc-demo .timeline-header.tx-b {
        color: var(--tx-b); background: var(--tx-b-bg);
        border: 1px solid var(--tx-b-border); border-bottom: none;
    }

    .rc-demo .timeline-body {
        border-radius: 0 0 var(--rc-radius) var(--rc-radius);
        min-height: 120px;
    }

    .rc-demo .timeline-body.tx-a { border: 1px solid var(--tx-a-border); border-top: none; }
    .rc-demo .timeline-body.tx-b { border: 1px solid var(--tx-b-border); border-top: none; }

    .rc-demo .step-card {
        padding: 0.5rem 0.75rem;
        border-bottom: 1px solid var(--rc-gray-100);
        transition: opacity 0.2s, background 0.2s;
    }

    .rc-demo .step-card:last-child { border-bottom: none; }
    .rc-demo .step-card.future { opacity: 0; pointer-events: none; height: 0; padding: 0; overflow: hidden; }
    .rc-demo .step-card.past { opacity: 0.45; }

    .rc-demo .step-card.current-a {
        background: var(--tx-a-bg); border-left: 3px solid var(--tx-a); opacity: 1;
    }

    .rc-demo .step-card.current-b {
        background: var(--tx-b-bg); border-left: 3px solid var(--tx-b); opacity: 1;
    }

    .rc-demo .step-card.idle {
        color: var(--rc-gray-400); font-style: italic; font-size: 0.8rem; padding: 0.35rem 0.75rem;
    }

    .rc-demo .sql {
        font-family: var(--rc-font-mono); font-size: 0.8rem;
        line-height: 1.5; word-break: break-word; white-space: pre-wrap;
    }

    .rc-demo .result {
        display: inline-block; font-family: var(--rc-font-mono); font-size: 0.75rem;
        padding: 0.15rem 0.5rem; border-radius: 4px; margin-top: 0.25rem; font-weight: 600;
    }

    .rc-demo .result-ok { background: var(--result-ok-bg); color: var(--result-ok); border: 1px solid #bbf7d0; }
    .rc-demo .result-warn { background: var(--result-warn-bg); color: var(--result-warn); border: 1px solid var(--tx-b-border); }

    .rc-demo .db-section { margin-bottom: 1.25rem; }

    .rc-demo .db-label {
        font-size: 0.75rem; font-weight: 600; text-transform: uppercase;
        letter-spacing: 0.05em; color: var(--rc-gray-500); margin-bottom: 0.4rem;
    }

    .rc-demo .db-label span { font-weight: 400; text-transform: none; letter-spacing: 0; }
    .rc-demo .db-table-wrap { overflow-x: auto; }

    .rc-demo .db-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; }

    .rc-demo .db-table th {
        text-align: left; padding: 0.4rem 0.6rem; background: var(--rc-gray-50);
        border: 1px solid var(--rc-gray-200); font-weight: 600; font-size: 0.75rem; color: var(--rc-gray-600);
    }

    .rc-demo .db-table th.mvcc-col { background: #f0f4ff; color: var(--rc-gray-500); font-size: 0.7rem; }

    .rc-demo .db-table td {
        padding: 0.4rem 0.6rem; border: 1px solid var(--rc-gray-200);
        font-family: var(--rc-font-mono); font-size: 0.8rem; transition: background 0.3s, opacity 0.3s;
    }

    .rc-demo .db-table td.mvcc-cell { font-size: 0.75rem; background: #fafbff; }
    .rc-demo .db-table tr.version-dead td { opacity: 0.4; text-decoration: line-through; }
    .rc-demo .db-table tr.version-dead td.mvcc-cell { text-decoration: none; }
    .rc-demo .db-table tr.version-seen-a { outline: 2px solid var(--tx-a); outline-offset: -1px; }
    .rc-demo .db-table tr.version-seen-b { outline: 2px solid var(--tx-b); outline-offset: -1px; }
    .rc-demo .db-table tr.version-uncommitted td { border-style: dashed; }

    .rc-demo .seen-badge {
        display: inline-block; font-family: var(--rc-font-sans); font-size: 0.65rem;
        font-weight: 600; padding: 0.1rem 0.35rem; border-radius: 3px;
        margin-left: 0.4rem; vertical-align: middle;
    }

    .rc-demo .seen-badge-a { background: var(--tx-a-bg); color: var(--tx-a); border: 1px solid var(--tx-a-border); }
    .rc-demo .seen-badge-b { background: var(--tx-b-bg); color: var(--tx-b); border: 1px solid var(--tx-b-border); }

    .rc-demo .txid-chip { display: inline-block; font-family: var(--rc-font-mono); font-size: 0.75rem; font-weight: 500; }
    .rc-demo .txid-chip.tx-old { color: var(--tx-old); }
    .rc-demo .txid-chip.tx-a-color { color: var(--tx-a); }
    .rc-demo .txid-chip.tx-b-color { color: var(--tx-b); }

    .rc-demo .committed-mark { color: var(--committed); font-size: 0.7rem; margin-left: 0.15rem; }
    .rc-demo .uncommitted-mark { color: var(--uncommitted); font-size: 0.65rem; margin-left: 0.15rem; font-style: italic; font-family: var(--rc-font-sans); }
    .rc-demo .xmax-empty { color: var(--rc-gray-300); }

    .rc-demo .explanation {
        background: var(--rc-gray-50); border: 1px solid var(--rc-gray-200);
        border-radius: var(--rc-radius); padding: 1rem 1.25rem;
        margin-bottom: 1.25rem; font-size: 0.9rem; line-height: 1.65; min-height: 3.5rem;
    }

    .rc-demo .explanation strong { color: var(--rc-gray-900); }
    .rc-demo .explanation .highlight { background: #fef9c3; padding: 0.1rem 0.3rem; border-radius: 3px; font-weight: 600; }
    .rc-demo .explanation code { font-family: var(--rc-font-mono); font-size: 0.85em; background: var(--rc-gray-100); padding: 0.1rem 0.3rem; border-radius: 3px; }

    .rc-demo .nav { display: flex; align-items: center; justify-content: center; gap: 1rem; }

    .rc-demo .nav-btn {
        display: inline-flex; align-items: center; gap: 0.35rem;
        padding: 0.5rem 1.1rem; border: 1px solid var(--rc-gray-300);
        border-radius: var(--rc-radius); background: #fff;
        font-family: var(--rc-font-sans); font-size: 0.85rem; font-weight: 500;
        color: var(--rc-gray-700); cursor: pointer;
        transition: background 0.15s, border-color 0.15s;
    }

    .rc-demo .nav-btn:hover:not(:disabled) { background: var(--rc-gray-50); border-color: var(--rc-gray-400); }
    .rc-demo .nav-btn:disabled { opacity: 0.35; cursor: default; }

    .rc-demo .step-indicator { font-size: 0.85rem; color: var(--rc-gray-500); font-weight: 500; min-width: 6rem; text-align: center; }

    .rc-demo .key-hint { text-align: center; margin-top: 0.5rem; font-size: 0.75rem; color: var(--rc-gray-400); }

    .rc-demo .key-hint kbd {
        display: inline-block; padding: 0.1rem 0.4rem; border: 1px solid var(--rc-gray-300);
        border-radius: 3px; background: var(--rc-gray-50); font-family: var(--rc-font-sans); font-size: 0.7rem;
    }

    @media (max-width: 640px) {
        .rc-demo .timelines { flex-direction: column; gap: 1rem; }
        .rc-demo .tabs { gap: 0; }
        .rc-demo .tab { padding: 0.5rem 0.6rem; font-size: 0.8rem; }
        .rc-demo .db-table { font-size: 0.75rem; }
        .rc-demo .db-table td, .rc-demo .db-table th { padding: 0.3rem 0.4rem; }
    }
</style>

<div class="rc-demo" id="rc-demo">
    <div class="rc-title">Read Committed: Interactive Demo</div>
    <p class="subtitle">Step-by-step visualization of concurrent transactions and MVCC</p>

    <div class="tabs" id="rc-tabs"></div>

    <div class="timelines">
        <div class="timeline">
            <div class="timeline-header tx-a" id="rc-header-a">Transaction A</div>
            <div class="timeline-body tx-a" id="rc-timeline-a"></div>
        </div>
        <div class="timeline">
            <div class="timeline-header tx-b" id="rc-header-b">Transaction B</div>
            <div class="timeline-body tx-b" id="rc-timeline-b"></div>
        </div>
    </div>

    <div class="db-section">
        <div class="db-label" id="rc-db-label">Row Versions on Disk</div>
        <div class="db-table-wrap">
            <table class="db-table" id="rc-db-table"></table>
        </div>
    </div>

    <div class="explanation" id="rc-explanation"></div>

    <div class="nav">
        <button class="nav-btn" id="rc-btn-back" disabled>&#9664; Back</button>
        <span class="step-indicator" id="rc-step-indicator">Step 1 of 7</span>
        <button class="nav-btn" id="rc-btn-fwd">Forward &#9654;</button>
    </div>
    <div class="key-hint">Use <kbd>&#8592;</kbd> <kbd>&#8594;</kbd> arrow keys to navigate</div>

</div>

<script>
(function() {
    var TX_OLD = 99, TX_A = 100, TX_B = 200;

    function v(xmin, xminC, xmax, xmaxC, data, seenBy, dead) {
        return { xmin: xmin, xminCommitted: xminC, xmax: xmax, xmaxCommitted: xmaxC, data: data, seenBy: seenBy || null, dead: dead || false };
    }

    var scenarios = [
        {
            id: 'non-repeatable-read', name: 'Non-repeatable Read', tableName: 'accounts',
            txAId: TX_A, txBId: TX_B, columns: ['id', 'name', 'balance'],
            steps: [
                { txA: { sql: 'BEGIN;' }, txB: null, versions: [ v(TX_OLD, true, null, null, [1, 'Alice', 1000], null, false) ], explanation: 'Transaction A begins (assigned <code>txid 100</code>). There is one row version on disk, created by an earlier committed transaction (<code>txid 99</code>).' },
                { txA: { sql: "SELECT balance FROM accounts\n  WHERE name = 'Alice';", result: '1000', resultType: 'ok' }, txB: null, versions: [ v(TX_OLD, true, null, null, [1, 'Alice', 1000], 'A', false) ], explanation: 'A takes a snapshot and reads the table. The version with <code>xmin=99</code> is committed and <code>xmax</code> is empty, so <strong>A sees balance = 1000</strong>.' },
                { txA: null, txB: { sql: 'BEGIN;' }, versions: [ v(TX_OLD, true, null, null, [1, 'Alice', 1000], null, false) ], explanation: 'Transaction B begins (assigned <code>txid 200</code>). Both transactions are now active concurrently.' },
                { txA: null, txB: { sql: "UPDATE accounts\n  SET balance = 500\n  WHERE name = 'Alice';" }, versions: [ v(TX_OLD, true, TX_B, false, [1, 'Alice', 1000], null, false), v(TX_B, false, null, null, [1, 'Alice', 500], null, false) ], explanation: 'B updates the row. PostgreSQL creates a <strong>new version</strong>. The old version gets <code>xmax=200</code>. The new version has <code>xmin=200</code>. Neither is committed yet.' },
                { txA: { sql: "SELECT balance FROM accounts\n  WHERE name = 'Alice';", result: '1000', resultType: 'ok' }, txB: null, versions: [ v(TX_OLD, true, TX_B, false, [1, 'Alice', 1000], 'A', false), v(TX_B, false, null, null, [1, 'Alice', 500], null, false) ], explanation: 'A takes a new snapshot. Old version: <code>xmin=99</code> committed, <code>xmax=200</code> not committed \u2014 row still alive. New version: <code>xmin=200</code> not committed \u2014 invisible. <strong>A reads 1000</strong>.' },
                { txA: null, txB: { sql: 'COMMIT;' }, versions: [ v(TX_OLD, true, TX_B, true, [1, 'Alice', 1000], null, true), v(TX_B, true, null, null, [1, 'Alice', 500], null, false) ], explanation: 'B commits. The old version is now <strong>dead</strong>. The new version is the live version.' },
                { txA: { sql: "SELECT balance FROM accounts\n  WHERE name = 'Alice';", result: '500', resultType: 'warn' }, txB: null, versions: [ v(TX_OLD, true, TX_B, true, [1, 'Alice', 1000], null, true), v(TX_B, true, null, null, [1, 'Alice', 500], 'A', false) ], explanation: 'A takes a new snapshot. <strong>A sees balance = 500.</strong> This is a <span class="highlight">non-repeatable read</span>: same query, different result.' }
            ]
        },
        {
            id: 'phantom-read', name: 'Phantom Read', tableName: 'orders',
            txAId: TX_A, txBId: TX_B, columns: ['id', 'product', 'status'],
            steps: [
                { txA: { sql: 'BEGIN;' }, txB: null, versions: [ v(TX_OLD, true, null, null, [1, 'Widget', 'pending'], null, false), v(TX_OLD, true, null, null, [2, 'Gadget', 'pending'], null, false), v(TX_OLD, true, null, null, [3, 'Gizmo', 'shipped'], null, false) ], explanation: 'Transaction A begins. The <code>orders</code> table has 3 rows. Two are <em>pending</em>, one is <em>shipped</em>.' },
                { txA: { sql: "SELECT * FROM orders\n  WHERE status = 'pending';", result: '2 rows', resultType: 'ok' }, txB: null, versions: [ v(TX_OLD, true, null, null, [1, 'Widget', 'pending'], 'A', false), v(TX_OLD, true, null, null, [2, 'Gadget', 'pending'], 'A', false), v(TX_OLD, true, null, null, [3, 'Gizmo', 'shipped'], null, false) ], explanation: 'A scans for pending orders. All versions visible. <strong>A gets 2 rows.</strong>' },
                { txA: null, txB: { sql: 'BEGIN;' }, versions: [ v(TX_OLD, true, null, null, [1, 'Widget', 'pending'], null, false), v(TX_OLD, true, null, null, [2, 'Gadget', 'pending'], null, false), v(TX_OLD, true, null, null, [3, 'Gizmo', 'shipped'], null, false) ], explanation: 'Transaction B begins.' },
                { txA: null, txB: { sql: "INSERT INTO orders\n  VALUES (4, 'Doohickey', 'pending');" }, versions: [ v(TX_OLD, true, null, null, [1, 'Widget', 'pending'], null, false), v(TX_OLD, true, null, null, [2, 'Gadget', 'pending'], null, false), v(TX_OLD, true, null, null, [3, 'Gizmo', 'shipped'], null, false), v(TX_B, false, null, null, [4, 'Doohickey', 'pending'], null, false) ], explanation: 'B inserts a new row with <code>xmin=200</code> (not yet committed).' },
                { txA: null, txB: { sql: 'COMMIT;' }, versions: [ v(TX_OLD, true, null, null, [1, 'Widget', 'pending'], null, false), v(TX_OLD, true, null, null, [2, 'Gadget', 'pending'], null, false), v(TX_OLD, true, null, null, [3, 'Gizmo', 'shipped'], null, false), v(TX_B, true, null, null, [4, 'Doohickey', 'pending'], null, false) ], explanation: 'B commits. The new row is now visible to future snapshots.' },
                { txA: { sql: "SELECT * FROM orders\n  WHERE status = 'pending';", result: '3 rows', resultType: 'warn' }, txB: null, versions: [ v(TX_OLD, true, null, null, [1, 'Widget', 'pending'], 'A', false), v(TX_OLD, true, null, null, [2, 'Gadget', 'pending'], 'A', false), v(TX_OLD, true, null, null, [3, 'Gizmo', 'shipped'], null, false), v(TX_B, true, null, null, [4, 'Doohickey', 'pending'], 'A', false) ], explanation: '<strong>A gets 3 pending rows!</strong> A row appeared that wasn\'t there before \u2014 this is a <span class="highlight">phantom read</span>.' }
            ]
        },
        {
            id: 'dirty-read-prevention', name: 'Dirty Read Prevented', tableName: 'accounts',
            txAId: TX_A, txBId: TX_B, columns: ['id', 'name', 'balance'],
            steps: [
                { txA: { sql: 'BEGIN;' }, txB: null, versions: [ v(TX_OLD, true, null, null, [1, 'Alice', 1000], null, false) ], explanation: 'Transaction A begins. Alice\'s balance is 1000.' },
                { txA: null, txB: { sql: 'BEGIN;' }, versions: [ v(TX_OLD, true, null, null, [1, 'Alice', 1000], null, false) ], explanation: 'Transaction B begins.' },
                { txA: null, txB: { sql: "UPDATE accounts\n  SET balance = 0\n  WHERE name = 'Alice';" }, versions: [ v(TX_OLD, true, TX_B, false, [1, 'Alice', 1000], null, false), v(TX_B, false, null, null, [1, 'Alice', 0], null, false) ], explanation: 'B updates the balance to 0. Two versions exist, neither change is committed.' },
                { txA: { sql: "SELECT balance FROM accounts\n  WHERE name = 'Alice';", result: '1000', resultType: 'ok' }, txB: null, versions: [ v(TX_OLD, true, TX_B, false, [1, 'Alice', 1000], 'A', false), v(TX_B, false, null, null, [1, 'Alice', 0], null, false) ], explanation: '<strong>A sees 1000. No dirty read!</strong> The uncommitted new version is invisible to A.' },
                { txA: null, txB: { sql: 'ROLLBACK;' }, versions: [ v(TX_OLD, true, null, null, [1, 'Alice', 1000], null, false) ], explanation: 'B rolls back. The new version is discarded.' },
                { txA: { sql: "SELECT balance FROM accounts\n  WHERE name = 'Alice';", result: '1000', resultType: 'ok' }, txB: null, versions: [ v(TX_OLD, true, null, null, [1, 'Alice', 1000], 'A', false) ], explanation: 'A reads <strong>1000</strong>. The rolled-back change never leaked. <span class="highlight">Read Committed kept us safe</span>.' }
            ]
        }
    ];

    var state = { scenarioIdx: 0, step: 0 };
    function cur() { return scenarios[state.scenarioIdx]; }
    function txidClass(t) { return t === TX_A ? 'tx-a-color' : t === TX_B ? 'tx-b-color' : 'tx-old'; }

    function renderTabs() {
        var c = document.getElementById('rc-tabs'); c.innerHTML = '';
        scenarios.forEach(function(s, i) {
            var b = document.createElement('button');
            b.className = 'tab' + (i === state.scenarioIdx ? ' active' : '');
            b.textContent = s.name;
            b.addEventListener('click', function() { state.scenarioIdx = i; state.step = 0; render(); });
            c.appendChild(b);
        });
    }

    function renderHeaders() {
        var s = cur();
        document.getElementById('rc-header-a').innerHTML = 'Transaction A <span class="txid">txid ' + s.txAId + '</span>';
        document.getElementById('rc-header-b').innerHTML = 'Transaction B <span class="txid">txid ' + s.txBId + '</span>';
    }

    function renderTimelines() {
        var s = cur();
        var aC = document.getElementById('rc-timeline-a'); aC.innerHTML = '';
        var bC = document.getElementById('rc-timeline-b'); bC.innerHTML = '';
        s.steps.forEach(function(sd, idx) {
            function mkCard(tx, side) {
                var card = document.createElement('div');
                if (tx) {
                    card.className = 'step-card';
                    if (idx < state.step) card.className += ' past';
                    else if (idx === state.step) card.className += ' current-' + side;
                    else card.className += ' future';
                    var sql = document.createElement('div'); sql.className = 'sql'; sql.textContent = tx.sql; card.appendChild(sql);
                    if (tx.result && idx <= state.step) {
                        var r = document.createElement('div'); r.className = 'result result-' + tx.resultType; r.textContent = '\u2192 ' + tx.result; card.appendChild(r);
                    }
                } else {
                    card.className = idx <= state.step ? 'step-card idle' : 'step-card future';
                    if (idx <= state.step) card.textContent = '\u2014';
                }
                return card;
            }
            aC.appendChild(mkCard(sd.txA, 'a'));
            bC.appendChild(mkCard(sd.txB, 'b'));
        });
    }

    function renderTable() {
        var s = cur(), sd = s.steps[state.step];
        document.getElementById('rc-db-label').innerHTML = s.tableName + ' <span>\u2014 MVCC row versions on disk</span>';
        var table = document.getElementById('rc-db-table'); table.innerHTML = '';
        var thead = document.createElement('thead'), hr = document.createElement('tr');
        ['xmin','xmax'].forEach(function(c){ var th=document.createElement('th'); th.className='mvcc-col'; th.textContent=c; hr.appendChild(th); });
        s.columns.forEach(function(c){ var th=document.createElement('th'); th.textContent=c; hr.appendChild(th); });
        var thV=document.createElement('th'); thV.className='mvcc-col'; thV.textContent=''; hr.appendChild(thV);
        thead.appendChild(hr); table.appendChild(thead);
        var tbody = document.createElement('tbody');
        sd.versions.forEach(function(ver) {
            var tr = document.createElement('tr'), cls = [];
            if (ver.dead) cls.push('version-dead');
            if (ver.seenBy === 'A') cls.push('version-seen-a');
            if (ver.seenBy === 'B') cls.push('version-seen-b');
            if (!ver.xminCommitted) cls.push('version-uncommitted');
            tr.className = cls.join(' ');
            // xmin
            var tdm = document.createElement('td'); tdm.className = 'mvcc-cell';
            var chip = document.createElement('span'); chip.className = 'txid-chip ' + txidClass(ver.xmin); chip.textContent = ver.xmin; tdm.appendChild(chip);
            if (ver.xminCommitted) { var m=document.createElement('span'); m.className='committed-mark'; m.textContent=' \u2714'; tdm.appendChild(m); }
            else { var m=document.createElement('span'); m.className='uncommitted-mark'; m.textContent=' pending'; tdm.appendChild(m); }
            tr.appendChild(tdm);
            // xmax
            var tdx = document.createElement('td'); tdx.className = 'mvcc-cell';
            if (ver.xmax !== null) {
                var cx=document.createElement('span'); cx.className='txid-chip '+txidClass(ver.xmax); cx.textContent=ver.xmax; tdx.appendChild(cx);
                if (ver.xmaxCommitted) { var mx=document.createElement('span'); mx.className='committed-mark'; mx.textContent=' \u2714'; tdx.appendChild(mx); }
                else { var mx=document.createElement('span'); mx.className='uncommitted-mark'; mx.textContent=' pending'; tdx.appendChild(mx); }
            } else { var em=document.createElement('span'); em.className='xmax-empty'; em.textContent='\u2014'; tdx.appendChild(em); }
            tr.appendChild(tdx);
            ver.data.forEach(function(val){ var td=document.createElement('td'); td.textContent=val; tr.appendChild(td); });
            var tdv = document.createElement('td'); tdv.className = 'mvcc-cell';
            if (ver.seenBy) { var badge=document.createElement('span'); badge.className='seen-badge seen-badge-'+ver.seenBy.toLowerCase(); badge.textContent='\u2190 '+ver.seenBy+' reads'; tdv.appendChild(badge); }
            tr.appendChild(tdv); tbody.appendChild(tr);
        });
        table.appendChild(tbody);
    }

    function renderNav() {
        var total = cur().steps.length;
        document.getElementById('rc-btn-back').disabled = state.step === 0;
        document.getElementById('rc-btn-fwd').disabled = state.step === total - 1;
        document.getElementById('rc-step-indicator').textContent = 'Step ' + (state.step + 1) + ' of ' + total;
    }

    function render() {
        renderTabs(); renderHeaders(); renderTimelines(); renderTable();
        document.getElementById('rc-explanation').innerHTML = cur().steps[state.step].explanation;
        renderNav();
    }

    document.getElementById('rc-btn-back').addEventListener('click', function() { if (state.step > 0) { state.step--; render(); } });
    document.getElementById('rc-btn-fwd').addEventListener('click', function() { if (state.step < cur().steps.length - 1) { state.step++; render(); } });

    var demo = document.getElementById('rc-demo');
    demo.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowLeft' && state.step > 0) { state.step--; render(); }
        if (e.key === 'ArrowRight' && state.step < cur().steps.length - 1) { state.step++; render(); }
    });
    demo.setAttribute('tabindex', '0');

    render();
})();
</script>

# 3. Isolation level: Repeatable Read

With Repeatable Read, all reads within a transaction see the database as of a single snapshot (a consistent version of data). This prevents non-repeatable reads and, in PostgreSQL, also prevents phantom reads within the transaction. (The SQL standard allows phantoms under Repeatable Read, but PostgreSQL’s implementation does not.)

However, this isolation level changes PostgreSQL’s behavior in an important way: some transactions may fail because PostgreSQL detects that completing them would violate the guarantees of the isolation level. This can happen, for example, when two concurrent transactions attempt to update the same row. In that case, once one transaction commits, the other may be forced to abort with a serialization-related error. The application must be prepared to decide whether the transaction can be retried.

It is useful to compare this with Read Committed. Under Read Committed, concurrent updates are typically resolved by waiting: one transaction waits for the other to commit or roll back, and then proceeds. After the lock is released, the second transaction can apply its update (assuming the update conditions still match).

PostgreSQL’s MVCC model also introduces a related anomaly under snapshot-based isolation: write skew. In write skew, two transactions read overlapping conditions and then perform updates that do not touch the same rows, but together violate a business rule. The database does not necessarily prevent this under Repeatable Read. This is often easiest to understand by testing practical examples.

<style>
    .rr-demo {
        --tx-a: #3b82f6;
        --tx-a-bg: #eff6ff;
        --tx-a-border: #bfdbfe;
        --tx-b: #f59e0b;
        --tx-b-bg: #fffbeb;
        --tx-b-border: #fde68a;
        --tx-old: #6b7280;
        --result-ok: #16a34a;
        --result-ok-bg: #f0fdf4;
        --result-warn: #d97706;
        --result-warn-bg: #fffbeb;
        --result-error: #dc2626;
        --result-error-bg: #fef2f2;
        --committed: #16a34a;
        --uncommitted: #9ca3af;
        --rr-gray-50: #f9fafb;
        --rr-gray-100: #f3f4f6;
        --rr-gray-200: #e5e7eb;
        --rr-gray-300: #d1d5db;
        --rr-gray-400: #9ca3af;
        --rr-gray-500: #6b7280;
        --rr-gray-600: #4b5563;
        --rr-gray-700: #374151;
        --rr-gray-800: #1f2937;
        --rr-gray-900: #111827;
        --rr-radius: 8px;
        --rr-font-mono: 'SF Mono', 'Fira Code', 'Fira Mono', Menlo, Consolas, monospace;
        --rr-font-sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    .rr-demo {
        font-family: var(--rr-font-sans);
        color: var(--rr-gray-800);
        line-height: 1.6;
        max-width: 900px;
        margin: 2rem auto;
        padding: 1.5rem;
        border: 1px solid var(--rr-gray-200);
        border-radius: var(--rr-radius);
        background: #fff;
    }

    .rr-demo .rr-title { font-size: 1.3rem; font-weight: 700; margin-bottom: 0.25rem; color: var(--rr-gray-900); }
    .rr-demo .subtitle { color: var(--rr-gray-500); font-size: 0.95rem; margin-bottom: 1.5rem; }

    .rr-demo .tabs { display: flex; gap: 0.25rem; border-bottom: 2px solid var(--rr-gray-200); margin-bottom: 1.5rem; overflow-x: auto; }
    .rr-demo .tab { padding: 0.6rem 1rem; border: none; background: none; font-family: var(--rr-font-sans); font-size: 0.875rem; font-weight: 500; color: var(--rr-gray-500); cursor: pointer; border-bottom: 2px solid transparent; margin-bottom: -2px; white-space: nowrap; transition: color 0.15s, border-color 0.15s; }
    .rr-demo .tab:hover { color: var(--rr-gray-700); }
    .rr-demo .tab.active { color: var(--tx-a); border-bottom-color: var(--tx-a); }

    .rr-demo .timelines { display: flex; gap: 1.5rem; margin-bottom: 1.5rem; }
    .rr-demo .timeline { flex: 1; min-width: 0; }
    .rr-demo .timeline-header { font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; padding: 0.4rem 0.75rem; border-radius: var(--rr-radius) var(--rr-radius) 0 0; margin-bottom: 0; }
    .rr-demo .timeline-header .txid { font-weight: 400; opacity: 0.7; font-size: 0.75rem; text-transform: none; letter-spacing: 0; }
    .rr-demo .timeline-header.tx-a { color: var(--tx-a); background: var(--tx-a-bg); border: 1px solid var(--tx-a-border); border-bottom: none; }
    .rr-demo .timeline-header.tx-b { color: var(--tx-b); background: var(--tx-b-bg); border: 1px solid var(--tx-b-border); border-bottom: none; }
    .rr-demo .timeline-body { border-radius: 0 0 var(--rr-radius) var(--rr-radius); min-height: 120px; }
    .rr-demo .timeline-body.tx-a { border: 1px solid var(--tx-a-border); border-top: none; }
    .rr-demo .timeline-body.tx-b { border: 1px solid var(--tx-b-border); border-top: none; }

    .rr-demo .step-card { padding: 0.5rem 0.75rem; border-bottom: 1px solid var(--rr-gray-100); transition: opacity 0.2s, background 0.2s; }
    .rr-demo .step-card:last-child { border-bottom: none; }
    .rr-demo .step-card.future { opacity: 0; pointer-events: none; height: 0; padding: 0; overflow: hidden; }
    .rr-demo .step-card.past { opacity: 0.45; }
    .rr-demo .step-card.current-a { background: var(--tx-a-bg); border-left: 3px solid var(--tx-a); opacity: 1; }
    .rr-demo .step-card.current-b { background: var(--tx-b-bg); border-left: 3px solid var(--tx-b); opacity: 1; }
    .rr-demo .step-card.idle { color: var(--rr-gray-400); font-style: italic; font-size: 0.8rem; padding: 0.35rem 0.75rem; }

    .rr-demo .sql { font-family: var(--rr-font-mono); font-size: 0.8rem; line-height: 1.5; word-break: break-word; white-space: pre-wrap; }
    .rr-demo .result { display: inline-block; font-family: var(--rr-font-mono); font-size: 0.75rem; padding: 0.15rem 0.5rem; border-radius: 4px; margin-top: 0.25rem; font-weight: 600; }
    .rr-demo .result-ok { background: var(--result-ok-bg); color: var(--result-ok); border: 1px solid #bbf7d0; }
    .rr-demo .result-warn { background: var(--result-warn-bg); color: var(--result-warn); border: 1px solid var(--tx-b-border); }
    .rr-demo .result-error { background: var(--result-error-bg); color: var(--result-error); border: 1px solid #fca5a5; }

    .rr-demo .snapshot-info { font-size: 0.8rem; padding: 0.5rem 0.75rem; background: #f0f4ff; border: 1px solid #dbeafe; border-radius: var(--rr-radius); margin-bottom: 0.75rem; color: var(--rr-gray-600); line-height: 1.5; display: none; }
    .rr-demo .snapshot-info.visible { display: block; }
    .rr-demo .snapshot-info code { font-family: var(--rr-font-mono); font-size: 0.8em; background: #e0e7ff; padding: 0.1rem 0.3rem; border-radius: 3px; }

    .rr-demo .db-section { margin-bottom: 1.25rem; }
    .rr-demo .db-label { font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: var(--rr-gray-500); margin-bottom: 0.4rem; }
    .rr-demo .db-label span { font-weight: 400; text-transform: none; letter-spacing: 0; }
    .rr-demo .db-table-wrap { overflow-x: auto; }
    .rr-demo .db-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; }
    .rr-demo .db-table th { text-align: left; padding: 0.4rem 0.6rem; background: var(--rr-gray-50); border: 1px solid var(--rr-gray-200); font-weight: 600; font-size: 0.75rem; color: var(--rr-gray-600); }
    .rr-demo .db-table th.mvcc-col { background: #f0f4ff; color: var(--rr-gray-500); font-size: 0.7rem; }
    .rr-demo .db-table td { padding: 0.4rem 0.6rem; border: 1px solid var(--rr-gray-200); font-family: var(--rr-font-mono); font-size: 0.8rem; transition: background 0.3s, opacity 0.3s; }
    .rr-demo .db-table td.mvcc-cell { font-size: 0.75rem; background: #fafbff; }
    .rr-demo .db-table tr.version-dead td { opacity: 0.4; text-decoration: line-through; }
    .rr-demo .db-table tr.version-dead td.mvcc-cell { text-decoration: none; }
    .rr-demo .db-table tr.version-seen-a { outline: 2px solid var(--tx-a); outline-offset: -1px; }
    .rr-demo .db-table tr.version-seen-b { outline: 2px solid var(--tx-b); outline-offset: -1px; }
    .rr-demo .db-table tr.version-uncommitted td { border-style: dashed; }

    .rr-demo .seen-badge { display: inline-block; font-family: var(--rr-font-sans); font-size: 0.65rem; font-weight: 600; padding: 0.1rem 0.35rem; border-radius: 3px; vertical-align: middle; }
    .rr-demo .seen-badge-a { background: var(--tx-a-bg); color: var(--tx-a); border: 1px solid var(--tx-a-border); }
    .rr-demo .seen-badge-b { background: var(--tx-b-bg); color: var(--tx-b); border: 1px solid var(--tx-b-border); }
    .rr-demo .version-note { display: block; font-family: var(--rr-font-sans); font-size: 0.6rem; color: var(--rr-gray-500); font-style: italic; margin-top: 0.15rem; }

    .rr-demo .txid-chip { display: inline-block; font-family: var(--rr-font-mono); font-size: 0.75rem; font-weight: 500; }
    .rr-demo .txid-chip.tx-old { color: var(--tx-old); }
    .rr-demo .txid-chip.tx-a-color { color: var(--tx-a); }
    .rr-demo .txid-chip.tx-b-color { color: var(--tx-b); }
    .rr-demo .committed-mark { color: var(--committed); font-size: 0.7rem; margin-left: 0.15rem; }
    .rr-demo .uncommitted-mark { color: var(--uncommitted); font-size: 0.65rem; margin-left: 0.15rem; font-style: italic; font-family: var(--rr-font-sans); }
    .rr-demo .xmax-empty { color: var(--rr-gray-300); }

    .rr-demo .explanation { background: var(--rr-gray-50); border: 1px solid var(--rr-gray-200); border-radius: var(--rr-radius); padding: 1rem 1.25rem; margin-bottom: 1.25rem; font-size: 0.9rem; line-height: 1.65; min-height: 3.5rem; }
    .rr-demo .explanation strong { color: var(--rr-gray-900); }
    .rr-demo .explanation .highlight { background: #fef9c3; padding: 0.1rem 0.3rem; border-radius: 3px; font-weight: 600; }
    .rr-demo .explanation .highlight-error { background: #fef2f2; color: var(--result-error); padding: 0.1rem 0.3rem; border-radius: 3px; font-weight: 600; }
    .rr-demo .explanation code { font-family: var(--rr-font-mono); font-size: 0.85em; background: var(--rr-gray-100); padding: 0.1rem 0.3rem; border-radius: 3px; }

    .rr-demo .nav { display: flex; align-items: center; justify-content: center; gap: 1rem; }
    .rr-demo .nav-btn { display: inline-flex; align-items: center; gap: 0.35rem; padding: 0.5rem 1.1rem; border: 1px solid var(--rr-gray-300); border-radius: var(--rr-radius); background: #fff; font-family: var(--rr-font-sans); font-size: 0.85rem; font-weight: 500; color: var(--rr-gray-700); cursor: pointer; transition: background 0.15s, border-color 0.15s; }
    .rr-demo .nav-btn:hover:not(:disabled) { background: var(--rr-gray-50); border-color: var(--rr-gray-400); }
    .rr-demo .nav-btn:disabled { opacity: 0.35; cursor: default; }
    .rr-demo .step-indicator { font-size: 0.85rem; color: var(--rr-gray-500); font-weight: 500; min-width: 6rem; text-align: center; }
    .rr-demo .key-hint { text-align: center; margin-top: 0.5rem; font-size: 0.75rem; color: var(--rr-gray-400); }
    .rr-demo .key-hint kbd { display: inline-block; padding: 0.1rem 0.4rem; border: 1px solid var(--rr-gray-300); border-radius: 3px; background: var(--rr-gray-50); font-family: var(--rr-font-sans); font-size: 0.7rem; }

    @media (max-width: 640px) {
        .rr-demo .timelines { flex-direction: column; gap: 1rem; }
        .rr-demo .tabs { gap: 0; }
        .rr-demo .tab { padding: 0.5rem 0.6rem; font-size: 0.8rem; }
        .rr-demo .db-table { font-size: 0.75rem; }
        .rr-demo .db-table td, .rr-demo .db-table th { padding: 0.3rem 0.4rem; }
    }
</style>

<div class="rr-demo" id="rr-demo">
    <div class="rr-title">Repeatable Read: Interactive Demo</div>
    <p class="subtitle">Snapshot isolation, serialization failures, and write skew</p>

    <div class="tabs" id="rr-tabs"></div>

    <div class="timelines">
        <div class="timeline">
            <div class="timeline-header tx-a" id="rr-header-a">Transaction A</div>
            <div class="timeline-body tx-a" id="rr-timeline-a"></div>
        </div>
        <div class="timeline">
            <div class="timeline-header tx-b" id="rr-header-b">Transaction B</div>
            <div class="timeline-body tx-b" id="rr-timeline-b"></div>
        </div>
    </div>

    <div class="snapshot-info" id="rr-snapshot-info"></div>

    <div class="db-section">
        <div class="db-label" id="rr-db-label">Row Versions on Disk</div>
        <div class="db-table-wrap">
            <table class="db-table" id="rr-db-table"></table>
        </div>
    </div>

    <div class="explanation" id="rr-explanation"></div>

    <div class="nav">
        <button class="nav-btn" id="rr-btn-back" disabled>&#9664; Back</button>
        <span class="step-indicator" id="rr-step-indicator">Step 1 of 7</span>
        <button class="nav-btn" id="rr-btn-fwd">Forward &#9654;</button>
    </div>
    <div class="key-hint">Use <kbd>&#8592;</kbd> <kbd>&#8594;</kbd> arrow keys to navigate</div>

</div>

<script>
(function() {
    var TX_OLD = 99, TX_A = 100, TX_B = 200;

    function v(xmin, xminC, xmax, xmaxC, data, seenBy, dead, note) {
        return { xmin: xmin, xminCommitted: xminC, xmax: xmax, xmaxCommitted: xmaxC, data: data, seenBy: seenBy || null, dead: dead || false, note: note || null };
    }

    var scenarios = [
        {
            id: 'snapshot-prevents-nonrepeatable', name: 'Non-repeatable Read Prevented', tableName: 'accounts',
            txAId: TX_A, txBId: TX_B, columns: ['id', 'name', 'balance'],
            steps: [
                { txA: { sql: 'BEGIN;' }, txB: null, snapshotInfo: null, versions: [ v(TX_OLD, true, null, null, [1, 'Alice', 1000]) ], explanation: 'Transaction A begins (<code>txid 100</code>). One row version on disk: Alice with balance 1000.' },
                { txA: { sql: "SELECT balance FROM accounts\n  WHERE name = 'Alice';", result: '1000', resultType: 'ok' }, txB: null, snapshotInfo: '<strong>A\'s snapshot taken now.</strong> It records: <code>txid 99</code> = committed. This snapshot will be reused for <em>every</em> subsequent statement in A.', versions: [ v(TX_OLD, true, null, null, [1, 'Alice', 1000], 'A') ], explanation: 'A executes its first query, which triggers a <strong>snapshot</strong>. Unlike Read Committed (which takes a new snapshot per statement), Repeatable Read takes <em>one snapshot</em> and reuses it for the entire transaction. A sees balance = 1000.' },
                { txA: null, txB: { sql: 'BEGIN;' }, snapshotInfo: 'A\'s snapshot (from step 2): <code>txid 200</code> does not exist in this snapshot.', versions: [ v(TX_OLD, true, null, null, [1, 'Alice', 1000]) ], explanation: 'Transaction B begins (<code>txid 200</code>). Note: txid 200 did not exist when A took its snapshot, so A will never see anything B does.' },
                { txA: null, txB: { sql: "UPDATE accounts\n  SET balance = 500\n  WHERE name = 'Alice';" }, snapshotInfo: 'A\'s snapshot (from step 2): <code>txid 200</code> is not visible.', versions: [ v(TX_OLD, true, TX_B, false, [1, 'Alice', 1000]), v(TX_B, false, null, null, [1, 'Alice', 500]) ], explanation: 'B updates the row. Old version gets <code>xmax=200</code> (pending). New version created with <code>xmin=200</code> (pending).' },
                { txA: null, txB: { sql: 'COMMIT;' }, snapshotInfo: 'A\'s snapshot (from step 2): <code>txid 200</code> is <strong>still not visible</strong> \u2014 it didn\'t exist when the snapshot was taken.', versions: [ v(TX_OLD, true, TX_B, true, [1, 'Alice', 1000], null, true), v(TX_B, true, null, null, [1, 'Alice', 500]) ], explanation: 'B commits. On disk, the old version is dead and the new version is live. But A\'s snapshot was taken <em>before</em> txid 200 existed \u2014 A will still treat 200 as invisible.' },
                { txA: { sql: "SELECT balance FROM accounts\n  WHERE name = 'Alice';", result: '1000', resultType: 'ok' }, txB: null, snapshotInfo: 'A\'s snapshot (from step 2): <code>txid 200</code> is not visible. A sees the old version as still alive.', versions: [ v(TX_OLD, true, TX_B, true, [1, 'Alice', 1000], 'A', false, 'A\'s snapshot: xmax not visible \u2192 alive'), v(TX_B, true, null, null, [1, 'Alice', 500], null, false, 'A\'s snapshot: xmin not visible \u2192 invisible') ], explanation: '<strong>A still sees balance = 1000!</strong> A reuses its snapshot from step 2. In that snapshot, txid 200 doesn\'t exist. <span class="highlight">Non-repeatable read prevented.</span> Under Read Committed, A would have seen 500 here.' }
            ]
        },
        {
            id: 'serialization-failure', name: 'Serialization Failure', tableName: 'accounts',
            txAId: TX_A, txBId: TX_B, columns: ['id', 'name', 'balance'],
            steps: [
                { txA: { sql: 'BEGIN;' }, txB: null, snapshotInfo: null, versions: [ v(TX_OLD, true, null, null, [1, 'Alice', 1000]) ], explanation: 'Transaction A begins. Alice has a balance of 1000.' },
                { txA: { sql: "SELECT balance FROM accounts\n  WHERE name = 'Alice';", result: '1000', resultType: 'ok' }, txB: null, snapshotInfo: '<strong>A\'s snapshot taken now.</strong> Only <code>txid 99</code> is committed.', versions: [ v(TX_OLD, true, null, null, [1, 'Alice', 1000], 'A') ], explanation: 'A reads Alice\'s balance: 1000. Snapshot taken.' },
                { txA: null, txB: { sql: 'BEGIN;' }, snapshotInfo: 'A\'s snapshot (from step 2): <code>txid 200</code> not visible.', versions: [ v(TX_OLD, true, null, null, [1, 'Alice', 1000]) ], explanation: 'Transaction B begins.' },
                { txA: null, txB: { sql: "UPDATE accounts\n  SET balance = 500\n  WHERE name = 'Alice';" }, snapshotInfo: 'A\'s snapshot (from step 2): <code>txid 200</code> not visible.', versions: [ v(TX_OLD, true, TX_B, false, [1, 'Alice', 1000]), v(TX_B, false, null, null, [1, 'Alice', 500]) ], explanation: 'B updates Alice\'s balance to 500.' },
                { txA: null, txB: { sql: 'COMMIT;' }, snapshotInfo: 'A\'s snapshot (from step 2): <code>txid 200</code> <strong>still not visible</strong>.', versions: [ v(TX_OLD, true, TX_B, true, [1, 'Alice', 1000], null, true), v(TX_B, true, null, null, [1, 'Alice', 500]) ], explanation: 'B commits. The row has been updated on disk. But A\'s snapshot still cannot see txid 200.' },
                { txA: { sql: "UPDATE accounts\n  SET balance = balance - 100\n  WHERE name = 'Alice';", result: 'ERROR: could not serialize access due to concurrent update', resultType: 'error' }, txB: null, snapshotInfo: 'A\'s snapshot (from step 2): <code>txid 200</code> not visible. But A tried to modify a row that 200 already changed.', versions: [ v(TX_OLD, true, TX_B, true, [1, 'Alice', 1000], null, true, 'A wanted to update this version'), v(TX_B, true, null, null, [1, 'Alice', 500], null, false, 'But txid 200 already replaced it') ], explanation: 'A tries to update Alice\'s row. PostgreSQL finds the version A can see has <code>xmax=200</code> which is now committed \u2014 someone else already modified this row after A\'s snapshot. <span class="highlight-error">ERROR: could not serialize access due to concurrent update.</span> A must ROLLBACK and retry.' }
            ]
        },
        {
            id: 'update-succeeds', name: 'No Row Conflict', tableName: 'accounts',
            txAId: TX_A, txBId: TX_B, columns: ['id', 'name', 'balance'],
            steps: [
                { txA: { sql: 'BEGIN;' }, txB: null, snapshotInfo: null, versions: [ v(TX_OLD, true, null, null, [1, 'Alice', 1000]), v(TX_OLD, true, null, null, [2, 'Bob', 2000]) ], explanation: 'Two accounts: Alice (1000) and Bob (2000). This time the transactions modify <strong>different rows</strong>.' },
                { txA: { sql: "SELECT balance FROM accounts\n  WHERE name = 'Alice';", result: '1000', resultType: 'ok' }, txB: null, snapshotInfo: '<strong>A\'s snapshot taken now.</strong>', versions: [ v(TX_OLD, true, null, null, [1, 'Alice', 1000], 'A'), v(TX_OLD, true, null, null, [2, 'Bob', 2000]) ], explanation: 'A reads Alice\'s balance: 1000. Snapshot taken.' },
                { txA: null, txB: { sql: 'BEGIN;' }, snapshotInfo: 'A\'s snapshot (from step 2): <code>txid 200</code> not visible.', versions: [ v(TX_OLD, true, null, null, [1, 'Alice', 1000]), v(TX_OLD, true, null, null, [2, 'Bob', 2000]) ], explanation: 'Transaction B begins.' },
                { txA: null, txB: { sql: "UPDATE accounts\n  SET balance = 1500\n  WHERE name = 'Bob';" }, snapshotInfo: 'A\'s snapshot (from step 2): <code>txid 200</code> not visible.', versions: [ v(TX_OLD, true, null, null, [1, 'Alice', 1000]), v(TX_OLD, true, TX_B, false, [2, 'Bob', 2000]), v(TX_B, false, null, null, [2, 'Bob', 1500]) ], explanation: 'B updates <strong>Bob\'s</strong> row (not Alice\'s).' },
                { txA: null, txB: { sql: 'COMMIT;' }, snapshotInfo: 'A\'s snapshot (from step 2): <code>txid 200</code> still not visible.', versions: [ v(TX_OLD, true, null, null, [1, 'Alice', 1000]), v(TX_OLD, true, TX_B, true, [2, 'Bob', 2000], null, true), v(TX_B, true, null, null, [2, 'Bob', 1500]) ], explanation: 'B commits. Bob\'s balance is now 1500 on disk.' },
                { txA: { sql: "UPDATE accounts\n  SET balance = 900\n  WHERE name = 'Alice';", result: 'UPDATE 1', resultType: 'ok' }, txB: null, snapshotInfo: 'A\'s snapshot (from step 2): <code>txid 200</code> not visible. But Alice\'s row is untouched \u2014 no conflict.', versions: [ v(TX_OLD, true, TX_A, false, [1, 'Alice', 1000]), v(TX_A, false, null, null, [1, 'Alice', 900]), v(TX_OLD, true, TX_B, true, [2, 'Bob', 2000], null, true), v(TX_B, true, null, null, [2, 'Bob', 1500]) ], explanation: 'A updates <strong>Alice\'s</strong> row. No one modified Alice\'s version since A\'s snapshot. <strong>No conflict!</strong> Compare this to the Serialization Failure tab.' },
                { txA: { sql: 'COMMIT;' }, txB: null, snapshotInfo: '<strong>Both committed successfully.</strong>', versions: [ v(TX_OLD, true, TX_A, true, [1, 'Alice', 1000], null, true), v(TX_A, true, null, null, [1, 'Alice', 900]), v(TX_OLD, true, TX_B, true, [2, 'Bob', 2000], null, true), v(TX_B, true, null, null, [2, 'Bob', 1500]) ], explanation: 'A commits. Both transactions succeeded: Alice=900, Bob=1500. The serialization failure only triggers when two transactions modify <strong>the same row</strong>. (Note: this can lead to write skew \u2014 see the next tab.)' }
            ]
        },
        {
            id: 'write-skew', name: 'Write Skew', tableName: 'doctors',
            txAId: TX_A, txBId: TX_B, columns: ['id', 'name', 'on_call'],
            steps: [
                { txA: { sql: 'BEGIN;' }, txB: null, snapshotInfo: null, versions: [ v(TX_OLD, true, null, null, [1, 'Alice', 'true']), v(TX_OLD, true, null, null, [2, 'Bob', 'true']) ], explanation: 'Two doctors are on call: Alice and Bob. The application requires <strong>at least one doctor on call</strong> at all times.' },
                { txA: { sql: "SELECT count(*) FROM doctors\n  WHERE on_call = true;", result: '2', resultType: 'ok' }, txB: null, snapshotInfo: '<strong>A\'s snapshot taken now.</strong> Sees both doctors on call.', versions: [ v(TX_OLD, true, null, null, [1, 'Alice', 'true'], 'A'), v(TX_OLD, true, null, null, [2, 'Bob', 'true'], 'A') ], explanation: 'A checks: 2 doctors on call. Alice decides she can safely go off call since Bob is still available.' },
                { txA: null, txB: { sql: 'BEGIN;' }, snapshotInfo: 'A\'s snapshot (from step 2): sees 2 doctors on call.', versions: [ v(TX_OLD, true, null, null, [1, 'Alice', 'true']), v(TX_OLD, true, null, null, [2, 'Bob', 'true']) ], explanation: 'Transaction B begins.' },
                { txA: null, txB: { sql: "SELECT count(*) FROM doctors\n  WHERE on_call = true;", result: '2', resultType: 'ok' }, snapshotInfo: 'A\'s snapshot: 2 on call. <strong>B\'s snapshot taken now</strong>: also 2 on call.', versions: [ v(TX_OLD, true, null, null, [1, 'Alice', 'true'], 'B'), v(TX_OLD, true, null, null, [2, 'Bob', 'true'], 'B') ], explanation: 'B checks: 2 doctors on call. Bob decides he can also go off call since Alice is still available.' },
                { txA: { sql: "UPDATE doctors SET on_call = false\n  WHERE name = 'Alice';" }, txB: null, snapshotInfo: 'A\'s snapshot: 2 on call. B\'s snapshot: 2 on call.', versions: [ v(TX_OLD, true, TX_A, false, [1, 'Alice', 'true']), v(TX_A, false, null, null, [1, 'Alice', 'false']), v(TX_OLD, true, null, null, [2, 'Bob', 'true']) ], explanation: 'A sets Alice off call. A modified <strong>row 1</strong> (Alice).' },
                { txA: null, txB: { sql: "UPDATE doctors SET on_call = false\n  WHERE name = 'Bob';" }, snapshotInfo: 'Each modifies a <strong>different row</strong> \u2014 no MVCC conflict.', versions: [ v(TX_OLD, true, TX_A, false, [1, 'Alice', 'true']), v(TX_A, false, null, null, [1, 'Alice', 'false']), v(TX_OLD, true, TX_B, false, [2, 'Bob', 'true']), v(TX_B, false, null, null, [2, 'Bob', 'false']) ], explanation: 'B sets Bob off call. B modified <strong>row 2</strong> (Bob). No conflict \u2014 different tuples.' },
                { txA: { sql: 'COMMIT;' }, txB: null, snapshotInfo: 'A commits.', versions: [ v(TX_OLD, true, TX_A, true, [1, 'Alice', 'true'], null, true), v(TX_A, true, null, null, [1, 'Alice', 'false']), v(TX_OLD, true, TX_B, false, [2, 'Bob', 'true']), v(TX_B, false, null, null, [2, 'Bob', 'false']) ], explanation: 'A commits. Alice is now off call.' },
                { txA: null, txB: { sql: 'COMMIT;' }, snapshotInfo: '<strong>Both committed successfully.</strong> No conflict was detected because they modified different rows.', versions: [ v(TX_OLD, true, TX_A, true, [1, 'Alice', 'true'], null, true), v(TX_A, true, null, null, [1, 'Alice', 'false']), v(TX_OLD, true, TX_B, true, [2, 'Bob', 'true'], null, true), v(TX_B, true, null, null, [2, 'Bob', 'false']) ], explanation: '<strong>B commits successfully!</strong> But look: Alice <code>on_call=false</code>, Bob <code>on_call=false</code>. <span class="highlight-error">Zero doctors on call. The constraint is violated.</span> This is a <span class="highlight">write skew</span> anomaly. Only the <strong>Serializable</strong> isolation level would prevent this.' }
            ]
        }
    ];

    var state = { scenarioIdx: 0, step: 0 };
    function cur() { return scenarios[state.scenarioIdx]; }
    function txidClass(t) { return t === TX_A ? 'tx-a-color' : t === TX_B ? 'tx-b-color' : 'tx-old'; }

    function renderTabs() {
        var c = document.getElementById('rr-tabs'); c.innerHTML = '';
        scenarios.forEach(function(s, i) {
            var b = document.createElement('button');
            b.className = 'tab' + (i === state.scenarioIdx ? ' active' : '');
            b.textContent = s.name;
            b.addEventListener('click', function() { state.scenarioIdx = i; state.step = 0; render(); });
            c.appendChild(b);
        });
    }

    function renderHeaders() {
        var s = cur();
        document.getElementById('rr-header-a').innerHTML = 'Transaction A <span class="txid">txid ' + s.txAId + '</span>';
        document.getElementById('rr-header-b').innerHTML = 'Transaction B <span class="txid">txid ' + s.txBId + '</span>';
    }

    function renderTimelines() {
        var s = cur();
        var aC = document.getElementById('rr-timeline-a'); aC.innerHTML = '';
        var bC = document.getElementById('rr-timeline-b'); bC.innerHTML = '';
        s.steps.forEach(function(sd, idx) {
            function mkCard(tx, side) {
                var card = document.createElement('div');
                if (tx) {
                    card.className = 'step-card';
                    if (idx < state.step) card.className += ' past';
                    else if (idx === state.step) card.className += ' current-' + side;
                    else card.className += ' future';
                    var sql = document.createElement('div'); sql.className = 'sql'; sql.textContent = tx.sql; card.appendChild(sql);
                    if (tx.result && idx <= state.step) {
                        var r = document.createElement('div'); r.className = 'result result-' + tx.resultType; r.textContent = '\u2192 ' + tx.result; card.appendChild(r);
                    }
                } else {
                    card.className = idx <= state.step ? 'step-card idle' : 'step-card future';
                    if (idx <= state.step) card.textContent = '\u2014';
                }
                return card;
            }
            aC.appendChild(mkCard(sd.txA, 'a'));
            bC.appendChild(mkCard(sd.txB, 'b'));
        });
    }

    function renderSnapshot() {
        var sd = cur().steps[state.step];
        var el = document.getElementById('rr-snapshot-info');
        if (sd.snapshotInfo) { el.innerHTML = sd.snapshotInfo; el.className = 'snapshot-info visible'; }
        else { el.className = 'snapshot-info'; el.innerHTML = ''; }
    }

    function renderTable() {
        var s = cur(), sd = s.steps[state.step];
        document.getElementById('rr-db-label').innerHTML = s.tableName + ' <span>\u2014 MVCC row versions on disk</span>';
        var table = document.getElementById('rr-db-table'); table.innerHTML = '';
        var thead = document.createElement('thead'), hr = document.createElement('tr');
        ['xmin','xmax'].forEach(function(c){ var th=document.createElement('th'); th.className='mvcc-col'; th.textContent=c; hr.appendChild(th); });
        s.columns.forEach(function(c){ var th=document.createElement('th'); th.textContent=c; hr.appendChild(th); });
        var thV=document.createElement('th'); thV.className='mvcc-col'; thV.textContent=''; hr.appendChild(thV);
        thead.appendChild(hr); table.appendChild(thead);
        var tbody = document.createElement('tbody');
        sd.versions.forEach(function(ver) {
            var tr = document.createElement('tr'), cls = [];
            if (ver.dead) cls.push('version-dead');
            if (ver.seenBy === 'A') cls.push('version-seen-a');
            if (ver.seenBy === 'B') cls.push('version-seen-b');
            if (!ver.xminCommitted) cls.push('version-uncommitted');
            tr.className = cls.join(' ');
            var tdm = document.createElement('td'); tdm.className = 'mvcc-cell';
            var chip = document.createElement('span'); chip.className = 'txid-chip ' + txidClass(ver.xmin); chip.textContent = ver.xmin; tdm.appendChild(chip);
            if (ver.xminCommitted) { var m=document.createElement('span'); m.className='committed-mark'; m.textContent=' \u2714'; tdm.appendChild(m); }
            else { var m=document.createElement('span'); m.className='uncommitted-mark'; m.textContent=' pending'; tdm.appendChild(m); }
            tr.appendChild(tdm);
            var tdx = document.createElement('td'); tdx.className = 'mvcc-cell';
            if (ver.xmax !== null) {
                var cx=document.createElement('span'); cx.className='txid-chip '+txidClass(ver.xmax); cx.textContent=ver.xmax; tdx.appendChild(cx);
                if (ver.xmaxCommitted) { var mx=document.createElement('span'); mx.className='committed-mark'; mx.textContent=' \u2714'; tdx.appendChild(mx); }
                else { var mx=document.createElement('span'); mx.className='uncommitted-mark'; mx.textContent=' pending'; tdx.appendChild(mx); }
            } else { var em=document.createElement('span'); em.className='xmax-empty'; em.textContent='\u2014'; tdx.appendChild(em); }
            tr.appendChild(tdx);
            ver.data.forEach(function(val){ var td=document.createElement('td'); td.textContent=val; tr.appendChild(td); });
            var tdv = document.createElement('td'); tdv.className = 'mvcc-cell';
            if (ver.seenBy) { var badge=document.createElement('span'); badge.className='seen-badge seen-badge-'+ver.seenBy.toLowerCase(); badge.textContent='\u2190 '+ver.seenBy+' reads'; tdv.appendChild(badge); }
            if (ver.note) { var noteEl=document.createElement('span'); noteEl.className='version-note'; noteEl.textContent=ver.note; tdv.appendChild(noteEl); }
            tr.appendChild(tdv); tbody.appendChild(tr);
        });
        table.appendChild(tbody);
    }

    function renderNav() {
        var total = cur().steps.length;
        document.getElementById('rr-btn-back').disabled = state.step === 0;
        document.getElementById('rr-btn-fwd').disabled = state.step === total - 1;
        document.getElementById('rr-step-indicator').textContent = 'Step ' + (state.step + 1) + ' of ' + total;
    }

    function render() {
        renderTabs(); renderHeaders(); renderTimelines(); renderSnapshot(); renderTable();
        document.getElementById('rr-explanation').innerHTML = cur().steps[state.step].explanation;
        renderNav();
    }

    document.getElementById('rr-btn-back').addEventListener('click', function() { if (state.step > 0) { state.step--; render(); } });
    document.getElementById('rr-btn-fwd').addEventListener('click', function() { if (state.step < cur().steps.length - 1) { state.step++; render(); } });

    var demo = document.getElementById('rr-demo');
    demo.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowLeft' && state.step > 0) { state.step--; render(); }
        if (e.key === 'ArrowRight' && state.step < cur().steps.length - 1) { state.step++; render(); }
    });
    demo.setAttribute('tabindex', '0');

    render();
})();
</script>

# 4. Isolation level: Serializable

The strongest isolation level is Serializable. It guarantees that concurrent transactions behave as if they were executed one-by-one in some order. In other words, the result must be equivalent to some serial execution; concurrent interleavings must not produce a different outcome.

In PostgreSQL, this is implemented using Serializable Snapshot Isolation (SSI). PostgreSQL tracks read/write dependencies (including predicate-level reads) to detect when concurrency could lead to a non-serializable outcome. When such a conflict is detected, PostgreSQL aborts one of the transactions to preserve serializability.

Serializable provides the strongest safety guarantees, but it is also the most expensive isolation level in terms of overhead and the likelihood of transaction retries. Just like Repeatable Read (and even more so), it requires the application to handle transaction aborts and implement a retry strategy when a serialization failure occurs.

<style>
    .sr-demo {
        --tx-a: #3b82f6;
        --tx-a-bg: #eff6ff;
        --tx-a-border: #bfdbfe;
        --tx-b: #f59e0b;
        --tx-b-bg: #fffbeb;
        --tx-b-border: #fde68a;
        --tx-old: #6b7280;
        --result-ok: #16a34a;
        --result-ok-bg: #f0fdf4;
        --result-warn: #d97706;
        --result-warn-bg: #fffbeb;
        --result-error: #dc2626;
        --result-error-bg: #fef2f2;
        --ssi: #7c3aed;
        --ssi-bg: #f5f3ff;
        --ssi-border: #ddd6fe;
        --committed: #16a34a;
        --uncommitted: #9ca3af;
        --sr-gray-50: #f9fafb;
        --sr-gray-100: #f3f4f6;
        --sr-gray-200: #e5e7eb;
        --sr-gray-300: #d1d5db;
        --sr-gray-400: #9ca3af;
        --sr-gray-500: #6b7280;
        --sr-gray-600: #4b5563;
        --sr-gray-700: #374151;
        --sr-gray-800: #1f2937;
        --sr-gray-900: #111827;
        --sr-radius: 8px;
        --sr-font-mono: 'SF Mono', 'Fira Code', 'Fira Mono', Menlo, Consolas, monospace;
        --sr-font-sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    .sr-demo {
        font-family: var(--sr-font-sans);
        color: var(--sr-gray-800);
        line-height: 1.6;
        max-width: 900px;
        margin: 2rem auto;
        padding: 1.5rem;
        border: 1px solid var(--sr-gray-200);
        border-radius: var(--sr-radius);
        background: #fff;
    }

    .sr-demo .sr-title { font-size: 1.3rem; font-weight: 700; margin-bottom: 0.25rem; color: var(--sr-gray-900); }
    .sr-demo .subtitle { color: var(--sr-gray-500); font-size: 0.95rem; margin-bottom: 1.5rem; }

    .sr-demo .tabs { display: flex; gap: 0.25rem; border-bottom: 2px solid var(--sr-gray-200); margin-bottom: 1.5rem; overflow-x: auto; }
    .sr-demo .tab { padding: 0.6rem 1rem; border: none; background: none; font-family: var(--sr-font-sans); font-size: 0.875rem; font-weight: 500; color: var(--sr-gray-500); cursor: pointer; border-bottom: 2px solid transparent; margin-bottom: -2px; white-space: nowrap; transition: color 0.15s, border-color 0.15s; }
    .sr-demo .tab:hover { color: var(--sr-gray-700); }
    .sr-demo .tab.active { color: var(--tx-a); border-bottom-color: var(--tx-a); }

    .sr-demo .timelines { display: flex; gap: 1.5rem; margin-bottom: 1.5rem; }
    .sr-demo .timeline { flex: 1; min-width: 0; }
    .sr-demo .timeline-header { font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; padding: 0.4rem 0.75rem; border-radius: var(--sr-radius) var(--sr-radius) 0 0; margin-bottom: 0; }
    .sr-demo .timeline-header .txid { font-weight: 400; opacity: 0.7; font-size: 0.75rem; text-transform: none; letter-spacing: 0; }
    .sr-demo .timeline-header.tx-a { color: var(--tx-a); background: var(--tx-a-bg); border: 1px solid var(--tx-a-border); border-bottom: none; }
    .sr-demo .timeline-header.tx-b { color: var(--tx-b); background: var(--tx-b-bg); border: 1px solid var(--tx-b-border); border-bottom: none; }
    .sr-demo .timeline-body { border-radius: 0 0 var(--sr-radius) var(--sr-radius); min-height: 120px; }
    .sr-demo .timeline-body.tx-a { border: 1px solid var(--tx-a-border); border-top: none; }
    .sr-demo .timeline-body.tx-b { border: 1px solid var(--tx-b-border); border-top: none; }

    .sr-demo .step-card { padding: 0.5rem 0.75rem; border-bottom: 1px solid var(--sr-gray-100); transition: opacity 0.2s, background 0.2s; }
    .sr-demo .step-card:last-child { border-bottom: none; }
    .sr-demo .step-card.future { opacity: 0; pointer-events: none; height: 0; padding: 0; overflow: hidden; }
    .sr-demo .step-card.past { opacity: 0.45; }
    .sr-demo .step-card.current-a { background: var(--tx-a-bg); border-left: 3px solid var(--tx-a); opacity: 1; }
    .sr-demo .step-card.current-b { background: var(--tx-b-bg); border-left: 3px solid var(--tx-b); opacity: 1; }
    .sr-demo .step-card.idle { color: var(--sr-gray-400); font-style: italic; font-size: 0.8rem; padding: 0.35rem 0.75rem; }

    .sr-demo .sql { font-family: var(--sr-font-mono); font-size: 0.8rem; line-height: 1.5; word-break: break-word; white-space: pre-wrap; }
    .sr-demo .result { display: inline-block; font-family: var(--sr-font-mono); font-size: 0.75rem; padding: 0.15rem 0.5rem; border-radius: 4px; margin-top: 0.25rem; font-weight: 600; }
    .sr-demo .result-ok { background: var(--result-ok-bg); color: var(--result-ok); border: 1px solid #bbf7d0; }
    .sr-demo .result-warn { background: var(--result-warn-bg); color: var(--result-warn); border: 1px solid var(--tx-b-border); }
    .sr-demo .result-error { background: var(--result-error-bg); color: var(--result-error); border: 1px solid #fca5a5; }

    .sr-demo .info-row { display: flex; gap: 0.75rem; margin-bottom: 0.75rem; }
    .sr-demo .snapshot-info, .sr-demo .ssi-info { font-size: 0.8rem; padding: 0.5rem 0.75rem; border-radius: var(--sr-radius); line-height: 1.5; display: none; flex: 1; }
    .sr-demo .snapshot-info.visible, .sr-demo .ssi-info.visible { display: block; }
    .sr-demo .snapshot-info { background: #f0f4ff; border: 1px solid #dbeafe; color: var(--sr-gray-600); }
    .sr-demo .ssi-info { background: var(--ssi-bg); border: 1px solid var(--ssi-border); color: var(--sr-gray-600); }
    .sr-demo .info-label { font-weight: 600; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.04em; display: block; margin-bottom: 0.2rem; }
    .sr-demo .snapshot-info .info-label { color: var(--tx-a); }
    .sr-demo .ssi-info .info-label { color: var(--ssi); }
    .sr-demo .snapshot-info code { font-family: var(--sr-font-mono); font-size: 0.8em; padding: 0.1rem 0.3rem; border-radius: 3px; background: #e0e7ff; }
    .sr-demo .ssi-info code { font-family: var(--sr-font-mono); font-size: 0.8em; padding: 0.1rem 0.3rem; border-radius: 3px; background: #ede9fe; }
    .sr-demo .dep-arrow { color: var(--ssi); font-weight: 600; }
    .sr-demo .dep-cycle { color: var(--result-error); font-weight: 700; }
    .sr-demo .dep-ok { color: var(--result-ok); font-weight: 600; }

    .sr-demo .db-section { margin-bottom: 1.25rem; }
    .sr-demo .db-label { font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: var(--sr-gray-500); margin-bottom: 0.4rem; }
    .sr-demo .db-label span { font-weight: 400; text-transform: none; letter-spacing: 0; }
    .sr-demo .db-table-wrap { overflow-x: auto; }
    .sr-demo .db-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; }
    .sr-demo .db-table th { text-align: left; padding: 0.4rem 0.6rem; background: var(--sr-gray-50); border: 1px solid var(--sr-gray-200); font-weight: 600; font-size: 0.75rem; color: var(--sr-gray-600); }
    .sr-demo .db-table th.mvcc-col { background: #f0f4ff; color: var(--sr-gray-500); font-size: 0.7rem; }
    .sr-demo .db-table td { padding: 0.4rem 0.6rem; border: 1px solid var(--sr-gray-200); font-family: var(--sr-font-mono); font-size: 0.8rem; transition: background 0.3s, opacity 0.3s; }
    .sr-demo .db-table td.mvcc-cell { font-size: 0.75rem; background: #fafbff; }
    .sr-demo .db-table tr.version-dead td { opacity: 0.4; text-decoration: line-through; }
    .sr-demo .db-table tr.version-dead td.mvcc-cell { text-decoration: none; }
    .sr-demo .db-table tr.version-seen-a { outline: 2px solid var(--tx-a); outline-offset: -1px; }
    .sr-demo .db-table tr.version-seen-b { outline: 2px solid var(--tx-b); outline-offset: -1px; }
    .sr-demo .db-table tr.version-uncommitted td { border-style: dashed; }

    .sr-demo .seen-badge { display: inline-block; font-family: var(--sr-font-sans); font-size: 0.65rem; font-weight: 600; padding: 0.1rem 0.35rem; border-radius: 3px; vertical-align: middle; }
    .sr-demo .seen-badge-a { background: var(--tx-a-bg); color: var(--tx-a); border: 1px solid var(--tx-a-border); }
    .sr-demo .seen-badge-b { background: var(--tx-b-bg); color: var(--tx-b); border: 1px solid var(--tx-b-border); }
    .sr-demo .version-note { display: block; font-family: var(--sr-font-sans); font-size: 0.6rem; color: var(--sr-gray-500); font-style: italic; margin-top: 0.15rem; }

    .sr-demo .txid-chip { display: inline-block; font-family: var(--sr-font-mono); font-size: 0.75rem; font-weight: 500; }
    .sr-demo .txid-chip.tx-old { color: var(--tx-old); }
    .sr-demo .txid-chip.tx-a-color { color: var(--tx-a); }
    .sr-demo .txid-chip.tx-b-color { color: var(--tx-b); }
    .sr-demo .committed-mark { color: var(--committed); font-size: 0.7rem; margin-left: 0.15rem; }
    .sr-demo .uncommitted-mark { color: var(--uncommitted); font-size: 0.65rem; margin-left: 0.15rem; font-style: italic; font-family: var(--sr-font-sans); }
    .sr-demo .xmax-empty { color: var(--sr-gray-300); }

    .sr-demo .explanation { background: var(--sr-gray-50); border: 1px solid var(--sr-gray-200); border-radius: var(--sr-radius); padding: 1rem 1.25rem; margin-bottom: 1.25rem; font-size: 0.9rem; line-height: 1.65; min-height: 3.5rem; }
    .sr-demo .explanation strong { color: var(--sr-gray-900); }
    .sr-demo .explanation .highlight { background: #fef9c3; padding: 0.1rem 0.3rem; border-radius: 3px; font-weight: 600; }
    .sr-demo .explanation .highlight-error { background: #fef2f2; color: var(--result-error); padding: 0.1rem 0.3rem; border-radius: 3px; font-weight: 600; }
    .sr-demo .explanation .highlight-ok { background: var(--result-ok-bg); color: var(--result-ok); padding: 0.1rem 0.3rem; border-radius: 3px; font-weight: 600; }
    .sr-demo .explanation code { font-family: var(--sr-font-mono); font-size: 0.85em; background: var(--sr-gray-100); padding: 0.1rem 0.3rem; border-radius: 3px; }

    .sr-demo .nav { display: flex; align-items: center; justify-content: center; gap: 1rem; }
    .sr-demo .nav-btn { display: inline-flex; align-items: center; gap: 0.35rem; padding: 0.5rem 1.1rem; border: 1px solid var(--sr-gray-300); border-radius: var(--sr-radius); background: #fff; font-family: var(--sr-font-sans); font-size: 0.85rem; font-weight: 500; color: var(--sr-gray-700); cursor: pointer; transition: background 0.15s, border-color 0.15s; }
    .sr-demo .nav-btn:hover:not(:disabled) { background: var(--sr-gray-50); border-color: var(--sr-gray-400); }
    .sr-demo .nav-btn:disabled { opacity: 0.35; cursor: default; }
    .sr-demo .step-indicator { font-size: 0.85rem; color: var(--sr-gray-500); font-weight: 500; min-width: 6rem; text-align: center; }
    .sr-demo .key-hint { text-align: center; margin-top: 0.5rem; font-size: 0.75rem; color: var(--sr-gray-400); }
    .sr-demo .key-hint kbd { display: inline-block; padding: 0.1rem 0.4rem; border: 1px solid var(--sr-gray-300); border-radius: 3px; background: var(--sr-gray-50); font-family: var(--sr-font-sans); font-size: 0.7rem; }

    @media (max-width: 640px) {
        .sr-demo .timelines { flex-direction: column; gap: 1rem; }
        .sr-demo .info-row { flex-direction: column; gap: 0.5rem; }
        .sr-demo .tabs { gap: 0; }
        .sr-demo .tab { padding: 0.5rem 0.6rem; font-size: 0.8rem; }
        .sr-demo .db-table { font-size: 0.75rem; }
        .sr-demo .db-table td, .sr-demo .db-table th { padding: 0.3rem 0.4rem; }
    }
</style>

<div class="sr-demo" id="sr-demo">
    <div class="sr-title">Serializable: Interactive Demo</div>
    <p class="subtitle">SSI predicate locking, dependency cycle detection, and true serializability</p>

    <div class="tabs" id="sr-tabs"></div>

    <div class="timelines">
        <div class="timeline">
            <div class="timeline-header tx-a" id="sr-header-a">Transaction A</div>
            <div class="timeline-body tx-a" id="sr-timeline-a"></div>
        </div>
        <div class="timeline">
            <div class="timeline-header tx-b" id="sr-header-b">Transaction B</div>
            <div class="timeline-body tx-b" id="sr-timeline-b"></div>
        </div>
    </div>

    <div class="info-row">
        <div class="snapshot-info" id="sr-snapshot-info"></div>
        <div class="ssi-info" id="sr-ssi-info"></div>
    </div>

    <div class="db-section">
        <div class="db-label" id="sr-db-label">Row Versions on Disk</div>
        <div class="db-table-wrap">
            <table class="db-table" id="sr-db-table"></table>
        </div>
    </div>

    <div class="explanation" id="sr-explanation"></div>

    <div class="nav">
        <button class="nav-btn" id="sr-btn-back" disabled>&#9664; Back</button>
        <span class="step-indicator" id="sr-step-indicator">Step 1 of 8</span>
        <button class="nav-btn" id="sr-btn-fwd">Forward &#9654;</button>
    </div>
    <div class="key-hint">Use <kbd>&#8592;</kbd> <kbd>&#8594;</kbd> arrow keys to navigate</div>

</div>

<script>
(function() {
    var TX_OLD = 99, TX_A = 100, TX_B = 200;

    function v(xmin, xminC, xmax, xmaxC, data, seenBy, dead, note) {
        return { xmin: xmin, xminCommitted: xminC, xmax: xmax, xmaxCommitted: xmaxC, data: data, seenBy: seenBy || null, dead: dead || false, note: note || null };
    }

    var scenarios = [
        {
            id: 'write-skew-prevented', name: 'Write Skew Prevented', tableName: 'doctors',
            txAId: TX_A, txBId: TX_B, columns: ['id', 'name', 'on_call'],
            steps: [
                { txA: { sql: 'BEGIN ISOLATION LEVEL SERIALIZABLE;' }, txB: null, snapshotInfo: null, ssiInfo: null, versions: [ v(TX_OLD, true, null, null, [1, 'Alice', 'true']), v(TX_OLD, true, null, null, [2, 'Bob', 'true']) ], explanation: 'Two doctors are on call. The rule: <strong>at least one must stay on call</strong>. Transaction A begins at Serializable isolation. (Under Repeatable Read, this same scenario would cause a write skew.)' },
                { txA: { sql: "SELECT count(*) FROM doctors\n  WHERE on_call = true;", result: '2', resultType: 'ok' }, txB: null, snapshotInfo: '<span class="info-label">Snapshots</span>A\'s snapshot taken. Sees both doctors on call.', ssiInfo: '<span class="info-label">SSI Predicate Locks</span>A: SIRead lock on <code>on_call = true</code>', versions: [ v(TX_OLD, true, null, null, [1, 'Alice', 'true'], 'A'), v(TX_OLD, true, null, null, [2, 'Bob', 'true'], 'A') ], explanation: 'A checks: 2 on call. SSI records a <strong>predicate lock</strong>: A has read all rows where <code>on_call = true</code>. Any future write to matching rows will create a dependency.' },
                { txA: null, txB: { sql: 'BEGIN ISOLATION LEVEL SERIALIZABLE;' }, snapshotInfo: '<span class="info-label">Snapshots</span>A: from step 2.', ssiInfo: '<span class="info-label">SSI Predicate Locks</span>A: SIRead on <code>on_call = true</code>', versions: [ v(TX_OLD, true, null, null, [1, 'Alice', 'true']), v(TX_OLD, true, null, null, [2, 'Bob', 'true']) ], explanation: 'Transaction B begins at Serializable isolation.' },
                { txA: null, txB: { sql: "SELECT count(*) FROM doctors\n  WHERE on_call = true;", result: '2', resultType: 'ok' }, snapshotInfo: '<span class="info-label">Snapshots</span>A: from step 2. B: taken now. Both see 2 on call.', ssiInfo: '<span class="info-label">SSI Predicate Locks</span>A: SIRead on <code>on_call = true</code><br>B: SIRead on <code>on_call = true</code>', versions: [ v(TX_OLD, true, null, null, [1, 'Alice', 'true'], 'B'), v(TX_OLD, true, null, null, [2, 'Bob', 'true'], 'B') ], explanation: 'B checks: 2 on call. SSI now tracks predicate locks for <em>both</em> transactions on the same predicate.' },
                { txA: { sql: "UPDATE doctors SET on_call = false\n  WHERE name = 'Alice';" }, txB: null, snapshotInfo: '<span class="info-label">Snapshots</span>A: from step 2. B: from step 4.', ssiInfo: '<span class="info-label">SSI Dependency Tracker</span>A writes Alice (<code>on_call: true \u2192 false</code>).<br>B has SIRead on <code>on_call = true</code> which covers Alice.<br><span class="dep-arrow">rw-dependency: B \u2192 A</span> (B read data A is modifying)', versions: [ v(TX_OLD, true, TX_A, false, [1, 'Alice', 'true']), v(TX_A, false, null, null, [1, 'Alice', 'false']), v(TX_OLD, true, null, null, [2, 'Bob', 'true']) ], explanation: 'A sets Alice off call. SSI detects a <strong>rw-dependency from B to A</strong> \u2014 B read data that A is changing.' },
                { txA: null, txB: { sql: "UPDATE doctors SET on_call = false\n  WHERE name = 'Bob';" }, snapshotInfo: '<span class="info-label">Snapshots</span>A: from step 2. B: from step 4.', ssiInfo: '<span class="info-label">SSI Dependency Tracker</span>B writes Bob (<code>on_call: true \u2192 false</code>).<br>A has SIRead on <code>on_call = true</code> which covers Bob.<br><span class="dep-arrow">rw-dependency: A \u2192 B</span> (A read data B is modifying)<br><span class="dep-cycle">\u26a0 Cycle: A \u2192 B \u2192 A</span>', versions: [ v(TX_OLD, true, TX_A, false, [1, 'Alice', 'true']), v(TX_A, false, null, null, [1, 'Alice', 'false']), v(TX_OLD, true, TX_B, false, [2, 'Bob', 'true']), v(TX_B, false, null, null, [2, 'Bob', 'false']) ], explanation: 'B sets Bob off call. SSI detects <strong>rw-dependency: A \u2192 B</strong>. Combined with B\u2192A: <span class="highlight-error">cycle detected: A \u2192 B \u2192 A</span>.' },
                { txA: { sql: 'COMMIT;' }, txB: null, snapshotInfo: '<span class="info-label">Snapshots</span>A committed. B: from step 4.', ssiInfo: '<span class="info-label">SSI Dependency Tracker</span><span class="dep-ok">A committed successfully</span> (first committer wins).<br><span class="dep-cycle">Cycle A \u2192 B \u2192 A still exists. B will fail.</span>', versions: [ v(TX_OLD, true, TX_A, true, [1, 'Alice', 'true'], null, true), v(TX_A, true, null, null, [1, 'Alice', 'false']), v(TX_OLD, true, TX_B, false, [2, 'Bob', 'true']), v(TX_B, false, null, null, [2, 'Bob', 'false']) ], explanation: 'A commits. The <strong>first committer wins</strong>. The cycle still exists, so B will be rejected.' },
                { txA: null, txB: { sql: 'COMMIT;', result: 'ERROR: could not serialize access due to read/write dependencies among transactions', resultType: 'error' }, snapshotInfo: '<span class="info-label">Snapshots</span>A: committed. B: aborted.', ssiInfo: '<span class="info-label">SSI Dependency Tracker</span><span class="dep-cycle">Cycle A \u2192 B \u2192 A \u2014 B must abort.</span><br>B\'s changes are discarded. B must retry.', versions: [ v(TX_OLD, true, TX_A, true, [1, 'Alice', 'true'], null, true), v(TX_A, true, null, null, [1, 'Alice', 'false']), v(TX_OLD, true, null, null, [2, 'Bob', 'true']) ], explanation: '<span class="highlight-error">B\'s commit is rejected!</span> SSI detected the cycle and aborted B. Bob is still on call. <span class="highlight">Serializable prevented the anomaly that Repeatable Read allowed.</span>' }
            ]
        },
        {
            id: 'rw-dependency-cycle', name: 'Dependency Cycle', tableName: 'config',
            txAId: TX_A, txBId: TX_B, columns: ['key', 'value'],
            steps: [
                { txA: { sql: 'BEGIN ISOLATION LEVEL SERIALIZABLE;' }, txB: null, snapshotInfo: null, ssiInfo: null, versions: [ v(TX_OLD, true, null, null, ['x', 1]), v(TX_OLD, true, null, null, ['y', 2]) ], explanation: 'A config table with <code>x=1</code> and <code>y=2</code>. A wants to copy x into y. B wants to copy y into x. In serial execution, the result is either (1,1) or (2,2) \u2014 never (2,1).' },
                { txA: { sql: "SELECT value FROM config\n  WHERE key = 'x';", result: '1', resultType: 'ok' }, txB: null, snapshotInfo: '<span class="info-label">Snapshots</span>A\'s snapshot taken.', ssiInfo: '<span class="info-label">SSI Predicate Locks</span>A: SIRead on <code>key = \'x\'</code>', versions: [ v(TX_OLD, true, null, null, ['x', 1], 'A'), v(TX_OLD, true, null, null, ['y', 2]) ], explanation: 'A reads <code>x = 1</code>. SSI tracks A\'s predicate lock on <code>key = \'x\'</code>.' },
                { txA: null, txB: { sql: 'BEGIN ISOLATION LEVEL SERIALIZABLE;' }, snapshotInfo: '<span class="info-label">Snapshots</span>A: from step 2.', ssiInfo: '<span class="info-label">SSI Predicate Locks</span>A: SIRead on <code>key = \'x\'</code>', versions: [ v(TX_OLD, true, null, null, ['x', 1]), v(TX_OLD, true, null, null, ['y', 2]) ], explanation: 'Transaction B begins.' },
                { txA: null, txB: { sql: "SELECT value FROM config\n  WHERE key = 'y';", result: '2', resultType: 'ok' }, snapshotInfo: '<span class="info-label">Snapshots</span>A: from step 2. B: taken now.', ssiInfo: '<span class="info-label">SSI Predicate Locks</span>A: SIRead on <code>key = \'x\'</code><br>B: SIRead on <code>key = \'y\'</code>', versions: [ v(TX_OLD, true, null, null, ['x', 1]), v(TX_OLD, true, null, null, ['y', 2], 'B') ], explanation: 'B reads <code>y = 2</code>. SSI tracks B\'s predicate lock on <code>key = \'y\'</code>.' },
                { txA: { sql: "UPDATE config SET value = 1\n  WHERE key = 'y';" }, txB: null, snapshotInfo: '<span class="info-label">Snapshots</span>A: from step 2. B: from step 4.', ssiInfo: '<span class="info-label">SSI Dependency Tracker</span>A writes <code>key = \'y\'</code>.<br>B has SIRead on <code>key = \'y\'</code>.<br><span class="dep-arrow">rw-dependency: B \u2192 A</span> (B read y, A writes y)', versions: [ v(TX_OLD, true, null, null, ['x', 1]), v(TX_OLD, true, TX_A, false, ['y', 2]), v(TX_A, false, null, null, ['y', 1]) ], explanation: 'A writes y=1. SSI detects: <strong>rw-dependency: B \u2192 A</strong>.' },
                { txA: null, txB: { sql: "UPDATE config SET value = 2\n  WHERE key = 'x';" }, snapshotInfo: '<span class="info-label">Snapshots</span>A: from step 2. B: from step 4.', ssiInfo: '<span class="info-label">SSI Dependency Tracker</span>B writes <code>key = \'x\'</code>.<br>A has SIRead on <code>key = \'x\'</code>.<br><span class="dep-arrow">rw-dependency: A \u2192 B</span> (A read x, B writes x)<br><span class="dep-cycle">\u26a0 Cycle: A \u2192 B \u2192 A</span>', versions: [ v(TX_OLD, true, TX_B, false, ['x', 1]), v(TX_B, false, null, null, ['x', 2]), v(TX_OLD, true, TX_A, false, ['y', 2]), v(TX_A, false, null, null, ['y', 1]) ], explanation: 'B writes x=2. SSI detects <strong>rw-dependency: A \u2192 B</strong>. <span class="highlight-error">Cycle: A \u2192 B \u2192 A</span>.' },
                { txA: { sql: 'COMMIT;' }, txB: null, snapshotInfo: '<span class="info-label">Snapshots</span>A: committed. B: from step 4.', ssiInfo: '<span class="info-label">SSI Dependency Tracker</span><span class="dep-ok">A committed (first committer wins).</span><br><span class="dep-cycle">Cycle A \u2192 B \u2192 A \u2014 B must abort.</span>', versions: [ v(TX_OLD, true, TX_B, false, ['x', 1]), v(TX_B, false, null, null, ['x', 2]), v(TX_OLD, true, TX_A, true, ['y', 2], null, true), v(TX_A, true, null, null, ['y', 1]) ], explanation: 'A commits: <code>y</code> is now 1. First committer wins.' },
                { txA: null, txB: { sql: 'COMMIT;', result: 'ERROR: could not serialize access due to read/write dependencies among transactions', resultType: 'error' }, snapshotInfo: '<span class="info-label">Snapshots</span>A: committed. B: aborted.', ssiInfo: '<span class="info-label">SSI Dependency Tracker</span><span class="dep-cycle">Cycle A \u2192 B \u2192 A \u2014 B aborted.</span>', versions: [ v(TX_OLD, true, null, null, ['x', 1]), v(TX_OLD, true, TX_A, true, ['y', 2], null, true), v(TX_A, true, null, null, ['y', 1]) ], explanation: '<span class="highlight-error">B is aborted.</span> Without Serializable, both would commit and produce <code>x=2, y=1</code> (swapped) \u2014 impossible in any serial execution. B can retry and will see <code>x=1</code>, producing <code>x=1, y=1</code>.' }
            ]
        },
        {
            id: 'safe-concurrent', name: 'Safe Concurrent Access', tableName: 'accounts',
            txAId: TX_A, txBId: TX_B, columns: ['id', 'name', 'balance'],
            steps: [
                { txA: { sql: 'BEGIN ISOLATION LEVEL SERIALIZABLE;' }, txB: null, snapshotInfo: null, ssiInfo: null, versions: [ v(TX_OLD, true, null, null, [1, 'Alice', 1000]), v(TX_OLD, true, null, null, [2, 'Bob', 2000]) ], explanation: 'Two accounts: Alice (1000) and Bob (2000). Each transaction independently withdraws from its own account. Serializable doesn\'t reject everything \u2014 let\'s see it allow safe concurrent access.' },
                { txA: { sql: "SELECT balance FROM accounts\n  WHERE name = 'Alice';", result: '1000', resultType: 'ok' }, txB: null, snapshotInfo: '<span class="info-label">Snapshots</span>A\'s snapshot taken.', ssiInfo: '<span class="info-label">SSI Predicate Locks</span>A: SIRead on <code>name = \'Alice\'</code>', versions: [ v(TX_OLD, true, null, null, [1, 'Alice', 1000], 'A'), v(TX_OLD, true, null, null, [2, 'Bob', 2000]) ], explanation: 'A reads Alice\'s balance: 1000.' },
                { txA: { sql: "UPDATE accounts SET balance = 900\n  WHERE name = 'Alice';" }, txB: null, snapshotInfo: '<span class="info-label">Snapshots</span>A: from step 2.', ssiInfo: '<span class="info-label">SSI Predicate Locks</span>A: SIRead on <code>name = \'Alice\'</code>, writes Alice.', versions: [ v(TX_OLD, true, TX_A, false, [1, 'Alice', 1000]), v(TX_A, false, null, null, [1, 'Alice', 900]), v(TX_OLD, true, null, null, [2, 'Bob', 2000]) ], explanation: 'A withdraws 100 from Alice. No cross-row dependency.' },
                { txA: null, txB: { sql: 'BEGIN ISOLATION LEVEL SERIALIZABLE;' }, snapshotInfo: '<span class="info-label">Snapshots</span>A: from step 2.', ssiInfo: '<span class="info-label">SSI Predicate Locks</span>A: SIRead on <code>name = \'Alice\'</code>, writes Alice.', versions: [ v(TX_OLD, true, TX_A, false, [1, 'Alice', 1000]), v(TX_A, false, null, null, [1, 'Alice', 900]), v(TX_OLD, true, null, null, [2, 'Bob', 2000]) ], explanation: 'Transaction B begins.' },
                { txA: null, txB: { sql: "SELECT balance FROM accounts\n  WHERE name = 'Bob';", result: '2000', resultType: 'ok' }, snapshotInfo: '<span class="info-label">Snapshots</span>A: from step 2. B: taken now.', ssiInfo: '<span class="info-label">SSI Predicate Locks</span>A: SIRead on <code>name = \'Alice\'</code>, writes Alice.<br>B: SIRead on <code>name = \'Bob\'</code><br><span class="dep-ok">No conflicts \u2014 different predicates, different rows.</span>', versions: [ v(TX_OLD, true, TX_A, false, [1, 'Alice', 1000]), v(TX_A, false, null, null, [1, 'Alice', 900]), v(TX_OLD, true, null, null, [2, 'Bob', 2000], 'B') ], explanation: 'B reads Bob\'s balance: 2000. <strong>No overlap</strong> with A\'s locks.' },
                { txA: null, txB: { sql: "UPDATE accounts SET balance = 1900\n  WHERE name = 'Bob';" }, snapshotInfo: '<span class="info-label">Snapshots</span>A: from step 2. B: from step 5.', ssiInfo: '<span class="info-label">SSI Dependency Tracker</span>A: reads Alice, writes Alice.<br>B: reads Bob, writes Bob.<br><span class="dep-ok">No rw-dependencies between A and B. No cycle possible.</span>', versions: [ v(TX_OLD, true, TX_A, false, [1, 'Alice', 1000]), v(TX_A, false, null, null, [1, 'Alice', 900]), v(TX_OLD, true, TX_B, false, [2, 'Bob', 2000]), v(TX_B, false, null, null, [2, 'Bob', 1900]) ], explanation: 'B withdraws 100 from Bob. No cross-dependencies exist.' },
                { txA: { sql: 'COMMIT;' }, txB: null, snapshotInfo: '<span class="info-label">Snapshots</span>A: committed. B: from step 5.', ssiInfo: '<span class="info-label">SSI Dependency Tracker</span><span class="dep-ok">A committed. No cycles detected.</span>', versions: [ v(TX_OLD, true, TX_A, true, [1, 'Alice', 1000], null, true), v(TX_A, true, null, null, [1, 'Alice', 900]), v(TX_OLD, true, TX_B, false, [2, 'Bob', 2000]), v(TX_B, false, null, null, [2, 'Bob', 1900]) ], explanation: 'A commits successfully. No dependency cycle.' },
                { txA: null, txB: { sql: 'COMMIT;' }, snapshotInfo: '<span class="info-label">Snapshots</span>A: committed. B: committed.', ssiInfo: '<span class="info-label">SSI Dependency Tracker</span><span class="dep-ok">B committed. No cycles. Both transactions succeeded.</span>', versions: [ v(TX_OLD, true, TX_A, true, [1, 'Alice', 1000], null, true), v(TX_A, true, null, null, [1, 'Alice', 900]), v(TX_OLD, true, TX_B, true, [2, 'Bob', 2000], null, true), v(TX_B, true, null, null, [2, 'Bob', 1900]) ], explanation: '<span class="highlight-ok">B commits successfully!</span> Alice: 900, Bob: 1900. Serializable is not overly restrictive \u2014 it only rejects transactions when it detects a genuine dependency cycle.' }
            ]
        }
    ];

    var state = { scenarioIdx: 0, step: 0 };
    function cur() { return scenarios[state.scenarioIdx]; }
    function txidClass(t) { return t === TX_A ? 'tx-a-color' : t === TX_B ? 'tx-b-color' : 'tx-old'; }

    function renderTabs() {
        var c = document.getElementById('sr-tabs'); c.innerHTML = '';
        scenarios.forEach(function(s, i) {
            var b = document.createElement('button');
            b.className = 'tab' + (i === state.scenarioIdx ? ' active' : '');
            b.textContent = s.name;
            b.addEventListener('click', function() { state.scenarioIdx = i; state.step = 0; render(); });
            c.appendChild(b);
        });
    }

    function renderHeaders() {
        var s = cur();
        document.getElementById('sr-header-a').innerHTML = 'Transaction A <span class="txid">txid ' + s.txAId + '</span>';
        document.getElementById('sr-header-b').innerHTML = 'Transaction B <span class="txid">txid ' + s.txBId + '</span>';
    }

    function renderTimelines() {
        var s = cur();
        var aC = document.getElementById('sr-timeline-a'); aC.innerHTML = '';
        var bC = document.getElementById('sr-timeline-b'); bC.innerHTML = '';
        s.steps.forEach(function(sd, idx) {
            function mkCard(tx, side) {
                var card = document.createElement('div');
                if (tx) {
                    card.className = 'step-card';
                    if (idx < state.step) card.className += ' past';
                    else if (idx === state.step) card.className += ' current-' + side;
                    else card.className += ' future';
                    var sql = document.createElement('div'); sql.className = 'sql'; sql.textContent = tx.sql; card.appendChild(sql);
                    if (tx.result && idx <= state.step) {
                        var r = document.createElement('div'); r.className = 'result result-' + tx.resultType; r.textContent = '\u2192 ' + tx.result; card.appendChild(r);
                    }
                } else {
                    card.className = idx <= state.step ? 'step-card idle' : 'step-card future';
                    if (idx <= state.step) card.textContent = '\u2014';
                }
                return card;
            }
            aC.appendChild(mkCard(sd.txA, 'a'));
            bC.appendChild(mkCard(sd.txB, 'b'));
        });
    }

    function renderInfoBanners() {
        var sd = cur().steps[state.step];
        var snapEl = document.getElementById('sr-snapshot-info');
        var ssiEl = document.getElementById('sr-ssi-info');
        if (sd.snapshotInfo) { snapEl.innerHTML = sd.snapshotInfo; snapEl.className = 'snapshot-info visible'; }
        else { snapEl.className = 'snapshot-info'; snapEl.innerHTML = ''; }
        if (sd.ssiInfo) { ssiEl.innerHTML = sd.ssiInfo; ssiEl.className = 'ssi-info visible'; }
        else { ssiEl.className = 'ssi-info'; ssiEl.innerHTML = ''; }
    }

    function renderTable() {
        var s = cur(), sd = s.steps[state.step];
        document.getElementById('sr-db-label').innerHTML = s.tableName + ' <span>\u2014 MVCC row versions on disk</span>';
        var table = document.getElementById('sr-db-table'); table.innerHTML = '';
        var thead = document.createElement('thead'), hr = document.createElement('tr');
        ['xmin','xmax'].forEach(function(c){ var th=document.createElement('th'); th.className='mvcc-col'; th.textContent=c; hr.appendChild(th); });
        s.columns.forEach(function(c){ var th=document.createElement('th'); th.textContent=c; hr.appendChild(th); });
        var thV=document.createElement('th'); thV.className='mvcc-col'; thV.textContent=''; hr.appendChild(thV);
        thead.appendChild(hr); table.appendChild(thead);
        var tbody = document.createElement('tbody');
        sd.versions.forEach(function(ver) {
            var tr = document.createElement('tr'), cls = [];
            if (ver.dead) cls.push('version-dead');
            if (ver.seenBy === 'A') cls.push('version-seen-a');
            if (ver.seenBy === 'B') cls.push('version-seen-b');
            if (!ver.xminCommitted) cls.push('version-uncommitted');
            tr.className = cls.join(' ');
            var tdm = document.createElement('td'); tdm.className = 'mvcc-cell';
            var chip = document.createElement('span'); chip.className = 'txid-chip ' + txidClass(ver.xmin); chip.textContent = ver.xmin; tdm.appendChild(chip);
            if (ver.xminCommitted) { var m=document.createElement('span'); m.className='committed-mark'; m.textContent=' \u2714'; tdm.appendChild(m); }
            else { var m=document.createElement('span'); m.className='uncommitted-mark'; m.textContent=' pending'; tdm.appendChild(m); }
            tr.appendChild(tdm);
            var tdx = document.createElement('td'); tdx.className = 'mvcc-cell';
            if (ver.xmax !== null) {
                var cx=document.createElement('span'); cx.className='txid-chip '+txidClass(ver.xmax); cx.textContent=ver.xmax; tdx.appendChild(cx);
                if (ver.xmaxCommitted) { var mx=document.createElement('span'); mx.className='committed-mark'; mx.textContent=' \u2714'; tdx.appendChild(mx); }
                else { var mx=document.createElement('span'); mx.className='uncommitted-mark'; mx.textContent=' pending'; tdx.appendChild(mx); }
            } else { var em=document.createElement('span'); em.className='xmax-empty'; em.textContent='\u2014'; tdx.appendChild(em); }
            tr.appendChild(tdx);
            ver.data.forEach(function(val){ var td=document.createElement('td'); td.textContent=val; tr.appendChild(td); });
            var tdv = document.createElement('td'); tdv.className = 'mvcc-cell';
            if (ver.seenBy) { var badge=document.createElement('span'); badge.className='seen-badge seen-badge-'+ver.seenBy.toLowerCase(); badge.textContent='\u2190 '+ver.seenBy+' reads'; tdv.appendChild(badge); }
            if (ver.note) { var noteEl=document.createElement('span'); noteEl.className='version-note'; noteEl.textContent=ver.note; tdv.appendChild(noteEl); }
            tr.appendChild(tdv); tbody.appendChild(tr);
        });
        table.appendChild(tbody);
    }

    function renderNav() {
        var total = cur().steps.length;
        document.getElementById('sr-btn-back').disabled = state.step === 0;
        document.getElementById('sr-btn-fwd').disabled = state.step === total - 1;
        document.getElementById('sr-step-indicator').textContent = 'Step ' + (state.step + 1) + ' of ' + total;
    }

    function render() {
        renderTabs(); renderHeaders(); renderTimelines(); renderInfoBanners(); renderTable();
        document.getElementById('sr-explanation').innerHTML = cur().steps[state.step].explanation;
        renderNav();
    }

    document.getElementById('sr-btn-back').addEventListener('click', function() { if (state.step > 0) { state.step--; render(); } });
    document.getElementById('sr-btn-fwd').addEventListener('click', function() { if (state.step < cur().steps.length - 1) { state.step++; render(); } });

    var demo = document.getElementById('sr-demo');
    demo.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowLeft' && state.step > 0) { state.step--; render(); }
        if (e.key === 'ArrowRight' && state.step < cur().steps.length - 1) { state.step++; render(); }
    });
    demo.setAttribute('tabindex', '0');

    render();
})();
</script>

# Interlude

Hopefully, the sections above explain why developers need to understand the different transaction isolation levels—and when it makes sense to use each of them.

At this point, it’s worth returning once more to the earlier discussion about Read Committed. There are practical techniques that let us keep using Read Committed while still avoiding many of its common pitfalls.

# Read Committed and locks

You might be getting a little tired of new concepts by now, but PostgreSQL gives us several tools that can help us avoid moving to higher isolation levels—and, importantly, avoid the transaction aborts that stronger levels (Repeatable Read / Serializable) may require you to handle with retry logic.

If we want to ensure that data we read cannot change during our transaction, we can add a locking clause to the query, such as FOR SHARE.

This prevents the selected rows from being modified while the lock is held. Any concurrent transaction that tries to update or delete those rows must wait until the current transaction completes.

A similar approach is FOR UPDATE, which takes a stronger lock. In addition to blocking updates and deletes, it also blocks other transactions from acquiring certain weaker locks on the same rows (including FOR SHARE-type locks). In other words: FOR UPDATE is more restrictive, and should be used only when you truly intend to update the locked rows (or when you intentionally want to serialize access).

Locks can also be used to prevent phantom reads, but only under specific access patterns. If two transactions protect a shared “guard row” (or some other shared resource) using SELECT ... FOR UPDATE, then inserts/updates that would otherwise create phantoms can be forced to wait—effectively serializing the critical section.

It’s also possible to use advisory locks to coordinate application-level critical sections. Advisory locks are powerful, but since they require careful design and consistent usage across the codebase, I’ll leave them as optional further reading.

To better understand how locks behave in practice, you can follow their effects in the interactive simulator below.

<style>
    .lk-demo {
        --tx-a: #3b82f6;
        --tx-a-bg: #eff6ff;
        --tx-a-border: #bfdbfe;
        --tx-b: #f59e0b;
        --tx-b-bg: #fffbeb;
        --tx-b-border: #fde68a;
        --tx-old: #6b7280;
        --result-ok: #16a34a;
        --result-ok-bg: #f0fdf4;
        --result-warn: #d97706;
        --result-warn-bg: #fffbeb;
        --result-error: #dc2626;
        --result-error-bg: #fef2f2;
        --result-blocked: #c2410c;
        --result-blocked-bg: #fff7ed;
        --lock: #0d9488;
        --lock-bg: #f0fdfa;
        --lock-border: #99f6e4;
        --committed: #16a34a;
        --uncommitted: #9ca3af;
        --lk-gray-50: #f9fafb;
        --lk-gray-100: #f3f4f6;
        --lk-gray-200: #e5e7eb;
        --lk-gray-300: #d1d5db;
        --lk-gray-400: #9ca3af;
        --lk-gray-500: #6b7280;
        --lk-gray-600: #4b5563;
        --lk-gray-700: #374151;
        --lk-gray-800: #1f2937;
        --lk-gray-900: #111827;
        --lk-radius: 8px;
        --lk-font-mono: 'SF Mono', 'Fira Code', 'Fira Mono', Menlo, Consolas, monospace;
        --lk-font-sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    .lk-demo {
        font-family: var(--lk-font-sans);
        color: var(--lk-gray-800);
        line-height: 1.6;
        max-width: 900px;
        margin: 2rem auto;
        padding: 1.5rem;
        border: 1px solid var(--lk-gray-200);
        border-radius: var(--lk-radius);
        background: #fff;
    }

    .lk-demo .lk-title { font-size: 1.3rem; font-weight: 700; margin-bottom: 0.25rem; color: var(--lk-gray-900); }
    .lk-demo .subtitle { color: var(--lk-gray-500); font-size: 0.95rem; margin-bottom: 1.5rem; }

    .lk-demo .tabs { display: flex; gap: 0.25rem; border-bottom: 2px solid var(--lk-gray-200); margin-bottom: 1.5rem; overflow-x: auto; }
    .lk-demo .tab { padding: 0.6rem 1rem; border: none; background: none; font-family: var(--lk-font-sans); font-size: 0.875rem; font-weight: 500; color: var(--lk-gray-500); cursor: pointer; border-bottom: 2px solid transparent; margin-bottom: -2px; white-space: nowrap; transition: color 0.15s, border-color 0.15s; }
    .lk-demo .tab:hover { color: var(--lk-gray-700); }
    .lk-demo .tab.active { color: var(--tx-a); border-bottom-color: var(--tx-a); }

    .lk-demo .timelines { display: flex; gap: 1.5rem; margin-bottom: 1.5rem; }
    .lk-demo .timeline { flex: 1; min-width: 0; }
    .lk-demo .timeline-header { font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; padding: 0.4rem 0.75rem; border-radius: var(--lk-radius) var(--lk-radius) 0 0; margin-bottom: 0; }
    .lk-demo .timeline-header .txid { font-weight: 400; opacity: 0.7; font-size: 0.75rem; text-transform: none; letter-spacing: 0; }
    .lk-demo .timeline-header.tx-a { color: var(--tx-a); background: var(--tx-a-bg); border: 1px solid var(--tx-a-border); border-bottom: none; }
    .lk-demo .timeline-header.tx-b { color: var(--tx-b); background: var(--tx-b-bg); border: 1px solid var(--tx-b-border); border-bottom: none; }
    .lk-demo .timeline-body { border-radius: 0 0 var(--lk-radius) var(--lk-radius); min-height: 120px; }
    .lk-demo .timeline-body.tx-a { border: 1px solid var(--tx-a-border); border-top: none; }
    .lk-demo .timeline-body.tx-b { border: 1px solid var(--tx-b-border); border-top: none; }

    .lk-demo .step-card { padding: 0.5rem 0.75rem; border-bottom: 1px solid var(--lk-gray-100); transition: opacity 0.2s, background 0.2s; }
    .lk-demo .step-card:last-child { border-bottom: none; }
    .lk-demo .step-card.future { opacity: 0; pointer-events: none; height: 0; padding: 0; overflow: hidden; }
    .lk-demo .step-card.past { opacity: 0.45; }
    .lk-demo .step-card.current-a { background: var(--tx-a-bg); border-left: 3px solid var(--tx-a); opacity: 1; }
    .lk-demo .step-card.current-b { background: var(--tx-b-bg); border-left: 3px solid var(--tx-b); opacity: 1; }
    .lk-demo .step-card.idle { color: var(--lk-gray-400); font-style: italic; font-size: 0.8rem; padding: 0.35rem 0.75rem; }

    .lk-demo .sql { font-family: var(--lk-font-mono); font-size: 0.8rem; line-height: 1.5; word-break: break-word; white-space: pre-wrap; }
    .lk-demo .result { display: inline-block; font-family: var(--lk-font-mono); font-size: 0.75rem; padding: 0.15rem 0.5rem; border-radius: 4px; margin-top: 0.25rem; font-weight: 600; }
    .lk-demo .result-ok { background: var(--result-ok-bg); color: var(--result-ok); border: 1px solid #bbf7d0; }
    .lk-demo .result-warn { background: var(--result-warn-bg); color: var(--result-warn); border: 1px solid var(--tx-b-border); }
    .lk-demo .result-error { background: var(--result-error-bg); color: var(--result-error); border: 1px solid #fca5a5; }
    .lk-demo .result-blocked { background: var(--result-blocked-bg); color: var(--result-blocked); border: 1px dashed #fdba74; animation: lk-pulse-blocked 2s infinite; }
    @keyframes lk-pulse-blocked { 0%, 100% { opacity: 1; } 50% { opacity: 0.6; } }

    .lk-demo .lock-info { font-size: 0.8rem; padding: 0.5rem 0.75rem; background: var(--lock-bg); border: 1px solid var(--lock-border); border-radius: var(--lk-radius); margin-bottom: 0.75rem; color: var(--lk-gray-600); line-height: 1.5; display: none; }
    .lk-demo .lock-info.visible { display: block; }
    .lk-demo .lock-info .info-label { font-weight: 600; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.04em; display: block; margin-bottom: 0.2rem; color: var(--lock); }
    .lk-demo .lock-info code { font-family: var(--lk-font-mono); font-size: 0.8em; background: #ccfbf1; padding: 0.1rem 0.3rem; border-radius: 3px; }
    .lk-demo .lock-held { color: var(--lock); font-weight: 600; }
    .lk-demo .lock-waiting { color: var(--result-blocked); font-weight: 600; }
    .lk-demo .lock-released { color: var(--lk-gray-400); }

    .lk-demo .db-section { margin-bottom: 1.25rem; }
    .lk-demo .db-label { font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: var(--lk-gray-500); margin-bottom: 0.4rem; }
    .lk-demo .db-label span { font-weight: 400; text-transform: none; letter-spacing: 0; }
    .lk-demo .db-table-wrap { overflow-x: auto; }
    .lk-demo .db-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; }
    .lk-demo .db-table th { text-align: left; padding: 0.4rem 0.6rem; background: var(--lk-gray-50); border: 1px solid var(--lk-gray-200); font-weight: 600; font-size: 0.75rem; color: var(--lk-gray-600); }
    .lk-demo .db-table th.mvcc-col { background: #f0f4ff; color: var(--lk-gray-500); font-size: 0.7rem; }
    .lk-demo .db-table td { padding: 0.4rem 0.6rem; border: 1px solid var(--lk-gray-200); font-family: var(--lk-font-mono); font-size: 0.8rem; transition: background 0.3s, opacity 0.3s; }
    .lk-demo .db-table td.mvcc-cell { font-size: 0.75rem; background: #fafbff; }
    .lk-demo .db-table tr.version-dead td { opacity: 0.4; text-decoration: line-through; }
    .lk-demo .db-table tr.version-dead td.mvcc-cell { text-decoration: none; }
    .lk-demo .db-table tr.version-seen-a { outline: 2px solid var(--tx-a); outline-offset: -1px; }
    .lk-demo .db-table tr.version-seen-b { outline: 2px solid var(--tx-b); outline-offset: -1px; }
    .lk-demo .db-table tr.version-uncommitted td { border-style: dashed; }

    .lk-demo .seen-badge { display: inline-block; font-family: var(--lk-font-sans); font-size: 0.65rem; font-weight: 600; padding: 0.1rem 0.35rem; border-radius: 3px; vertical-align: middle; }
    .lk-demo .seen-badge-a { background: var(--tx-a-bg); color: var(--tx-a); border: 1px solid var(--tx-a-border); }
    .lk-demo .seen-badge-b { background: var(--tx-b-bg); color: var(--tx-b); border: 1px solid var(--tx-b-border); }
    .lk-demo .lock-badge { display: inline-block; font-family: var(--lk-font-sans); font-size: 0.6rem; font-weight: 600; padding: 0.1rem 0.35rem; border-radius: 3px; vertical-align: middle; margin-left: 0.3rem; background: var(--lock-bg); color: var(--lock); border: 1px solid var(--lock-border); }
    .lk-demo .lock-badge-waiting { background: var(--result-blocked-bg); color: var(--result-blocked); border: 1px dashed #fdba74; }
    .lk-demo .version-note { display: block; font-family: var(--lk-font-sans); font-size: 0.6rem; color: var(--lk-gray-500); font-style: italic; margin-top: 0.15rem; }

    .lk-demo .txid-chip { display: inline-block; font-family: var(--lk-font-mono); font-size: 0.75rem; font-weight: 500; }
    .lk-demo .txid-chip.tx-old { color: var(--tx-old); }
    .lk-demo .txid-chip.tx-a-color { color: var(--tx-a); }
    .lk-demo .txid-chip.tx-b-color { color: var(--tx-b); }
    .lk-demo .committed-mark { color: var(--committed); font-size: 0.7rem; margin-left: 0.15rem; }
    .lk-demo .uncommitted-mark { color: var(--uncommitted); font-size: 0.65rem; margin-left: 0.15rem; font-style: italic; font-family: var(--lk-font-sans); }
    .lk-demo .xmax-empty { color: var(--lk-gray-300); }

    .lk-demo .explanation { background: var(--lk-gray-50); border: 1px solid var(--lk-gray-200); border-radius: var(--lk-radius); padding: 1rem 1.25rem; margin-bottom: 1.25rem; font-size: 0.9rem; line-height: 1.65; min-height: 3.5rem; }
    .lk-demo .explanation strong { color: var(--lk-gray-900); }
    .lk-demo .explanation .highlight { background: #fef9c3; padding: 0.1rem 0.3rem; border-radius: 3px; font-weight: 600; }
    .lk-demo .explanation .highlight-ok { background: var(--result-ok-bg); color: var(--result-ok); padding: 0.1rem 0.3rem; border-radius: 3px; font-weight: 600; }
    .lk-demo .explanation code { font-family: var(--lk-font-mono); font-size: 0.85em; background: var(--lk-gray-100); padding: 0.1rem 0.3rem; border-radius: 3px; }

    .lk-demo .nav { display: flex; align-items: center; justify-content: center; gap: 1rem; }
    .lk-demo .nav-btn { display: inline-flex; align-items: center; gap: 0.35rem; padding: 0.5rem 1.1rem; border: 1px solid var(--lk-gray-300); border-radius: var(--lk-radius); background: #fff; font-family: var(--lk-font-sans); font-size: 0.85rem; font-weight: 500; color: var(--lk-gray-700); cursor: pointer; transition: background 0.15s, border-color 0.15s; }
    .lk-demo .nav-btn:hover:not(:disabled) { background: var(--lk-gray-50); border-color: var(--lk-gray-400); }
    .lk-demo .nav-btn:disabled { opacity: 0.35; cursor: default; }
    .lk-demo .step-indicator { font-size: 0.85rem; color: var(--lk-gray-500); font-weight: 500; min-width: 6rem; text-align: center; }
    .lk-demo .key-hint { text-align: center; margin-top: 0.5rem; font-size: 0.75rem; color: var(--lk-gray-400); }
    .lk-demo .key-hint kbd { display: inline-block; padding: 0.1rem 0.4rem; border: 1px solid var(--lk-gray-300); border-radius: 3px; background: var(--lk-gray-50); font-family: var(--lk-font-sans); font-size: 0.7rem; }

    @media (max-width: 640px) {
        .lk-demo .timelines { flex-direction: column; gap: 1rem; }
        .lk-demo .tabs { gap: 0; }
        .lk-demo .tab { padding: 0.5rem 0.6rem; font-size: 0.8rem; }
        .lk-demo .db-table { font-size: 0.75rem; }
        .lk-demo .db-table td, .lk-demo .db-table th { padding: 0.3rem 0.4rem; }
    }
</style>

<div class="lk-demo" id="lk-demo">
    <div class="lk-title">Read Committed: Avoiding Anomalies with Explicit Locks</div>
    <p class="subtitle">Using FOR SHARE and FOR UPDATE to get stronger guarantees without changing isolation level</p>

    <div class="tabs" id="lk-tabs"></div>

    <div class="timelines">
        <div class="timeline">
            <div class="timeline-header tx-a" id="lk-header-a">Transaction A</div>
            <div class="timeline-body tx-a" id="lk-timeline-a"></div>
        </div>
        <div class="timeline">
            <div class="timeline-header tx-b" id="lk-header-b">Transaction B</div>
            <div class="timeline-body tx-b" id="lk-timeline-b"></div>
        </div>
    </div>

    <div class="lock-info" id="lk-lock-info"></div>

    <div class="db-section">
        <div class="db-label" id="lk-db-label">Row Versions on Disk</div>
        <div class="db-table-wrap">
            <table class="db-table" id="lk-db-table"></table>
        </div>
    </div>

    <div class="explanation" id="lk-explanation"></div>

    <div class="nav">
        <button class="nav-btn" id="lk-btn-back" disabled>&#9664; Back</button>
        <span class="step-indicator" id="lk-step-indicator">Step 1 of 8</span>
        <button class="nav-btn" id="lk-btn-fwd">Forward &#9654;</button>
    </div>
    <div class="key-hint">Use <kbd>&#8592;</kbd> <kbd>&#8594;</kbd> arrow keys to navigate</div>

</div>

<script>
(function() {
    var TX_OLD = 99, TX_A = 100, TX_B = 200;

    function v(xmin, xminC, xmax, xmaxC, data, seenBy, dead, note, lock) {
        return { xmin: xmin, xminCommitted: xminC, xmax: xmax, xmaxCommitted: xmaxC, data: data, seenBy: seenBy || null, dead: dead || false, note: note || null, lock: lock || null };
    }

    var scenarios = [
        {
            id: 'for-share-nonrepeatable', name: 'FOR SHARE', tableName: 'accounts',
            txAId: TX_A, txBId: TX_B, columns: ['id', 'name', 'balance'],
            steps: [
                { txA: { sql: 'BEGIN;' }, txB: null, lockInfo: null, versions: [ v(TX_OLD, true, null, null, [1, 'Alice', 1000]) ], explanation: 'Without locking, Read Committed allows non-repeatable reads: a second SELECT can return different data if another transaction commits in between. <code>FOR SHARE</code> prevents this by blocking other transactions from modifying the locked rows.' },
                { txA: { sql: "SELECT balance FROM accounts\n  WHERE name = 'Alice'\n  FOR SHARE;", result: '1000', resultType: 'ok' }, txB: null, lockInfo: '<span class="info-label">Row Locks</span><span class="lock-held">A: FOR SHARE on (Alice, 1000)</span> \u2014 others can read, but cannot UPDATE or DELETE this row until A commits.', versions: [ v(TX_OLD, true, null, null, [1, 'Alice', 1000], 'A', false, null, 'lock-a') ], explanation: 'A reads Alice\'s balance with <code>FOR SHARE</code>. This acquires a <strong>row-level SHARE lock</strong>. Other transactions can still read the row, but any attempt to UPDATE or DELETE will block until A releases the lock (at COMMIT or ROLLBACK).' },
                { txA: null, txB: { sql: 'BEGIN;' }, lockInfo: '<span class="info-label">Row Locks</span><span class="lock-held">A: FOR SHARE on (Alice, 1000)</span>', versions: [ v(TX_OLD, true, null, null, [1, 'Alice', 1000], null, false, null, 'lock-a') ], explanation: 'Transaction B begins.' },
                { txA: null, txB: { sql: "UPDATE accounts SET balance = 500\n  WHERE name = 'Alice';", result: 'BLOCKED \u2014 waiting for A\'s lock', resultType: 'blocked' }, lockInfo: '<span class="info-label">Row Locks</span><span class="lock-held">A: FOR SHARE on (Alice, 1000)</span><br><span class="lock-waiting">B: waiting for exclusive lock on Alice (blocked by A\'s SHARE lock)</span>', versions: [ v(TX_OLD, true, null, null, [1, 'Alice', 1000], null, false, null, 'lock-a') ], explanation: 'B tries to UPDATE Alice\'s row. The UPDATE needs an exclusive lock, but A holds a SHARE lock. <strong>B is blocked</strong> \u2014 it must wait until A commits or rolls back. The row is unchanged on disk.' },
                { txA: { sql: "SELECT balance FROM accounts\n  WHERE name = 'Alice';", result: '1000', resultType: 'ok' }, txB: null, lockInfo: '<span class="info-label">Row Locks</span><span class="lock-held">A: FOR SHARE on (Alice, 1000)</span><br><span class="lock-waiting">B: still waiting</span>', versions: [ v(TX_OLD, true, null, null, [1, 'Alice', 1000], 'A', false, null, 'lock-a') ], explanation: 'A reads Alice\'s balance again \u2014 <strong>still 1000</strong>. Because B is blocked by the lock, the row hasn\'t changed. This is a plain SELECT (no FOR SHARE needed for the re-read). <span class="highlight">Non-repeatable read prevented</span> \u2014 the lock guarantees consistency within A\'s transaction.' },
                { txA: { sql: 'COMMIT;' }, txB: null, lockInfo: '<span class="info-label">Row Locks</span><span class="lock-released">A: lock released</span><br><span class="lock-held">B: unblocked \u2014 acquires exclusive lock</span>', versions: [ v(TX_OLD, true, null, null, [1, 'Alice', 1000]) ], explanation: 'A commits, releasing the SHARE lock. B is unblocked and its UPDATE can now proceed.' },
                { txA: null, txB: { sql: '(UPDATE proceeds)', result: 'UPDATE 1', resultType: 'ok' }, lockInfo: '<span class="info-label">Row Locks</span><span class="lock-held">B: exclusive lock on Alice</span>', versions: [ v(TX_OLD, true, TX_B, false, [1, 'Alice', 1000]), v(TX_B, false, null, null, [1, 'Alice', 500], null, false, null, 'lock-b') ], explanation: 'B\'s UPDATE finally executes. A new version is created with balance = 500.' },
                { txA: null, txB: { sql: 'COMMIT;' }, lockInfo: '<span class="info-label">Row Locks</span><span class="lock-released">All locks released.</span>', versions: [ v(TX_OLD, true, TX_B, true, [1, 'Alice', 1000], null, true), v(TX_B, true, null, null, [1, 'Alice', 500]) ], explanation: 'B commits. Final balance: 500. The key point: <code>FOR SHARE</code> gave A a consistent view of the data throughout its transaction by preventing concurrent modifications, without needing to change the isolation level.' }
            ]
        },
        {
            id: 'for-update-lost-update', name: 'FOR UPDATE', tableName: 'accounts',
            txAId: TX_A, txBId: TX_B, columns: ['id', 'name', 'balance'],
            steps: [
                { txA: { sql: 'BEGIN;' }, txB: null, lockInfo: null, versions: [ v(TX_OLD, true, null, null, [1, 'Alice', 1000]) ], explanation: 'Classic lost update scenario: two transactions both want to decrement Alice\'s balance by 100. Without locking, one update would overwrite the other. <code>FOR UPDATE</code> prevents this.' },
                { txA: { sql: "SELECT balance FROM accounts\n  WHERE name = 'Alice'\n  FOR UPDATE;", result: '1000', resultType: 'ok' }, txB: null, lockInfo: '<span class="info-label">Row Locks</span><span class="lock-held">A: FOR UPDATE on (Alice, 1000)</span> \u2014 exclusive lock, no one else can read FOR UPDATE/SHARE or modify this row.', versions: [ v(TX_OLD, true, null, null, [1, 'Alice', 1000], 'A', false, null, 'lock-a') ], explanation: 'A reads balance with <code>FOR UPDATE</code>, acquiring an <strong>exclusive row lock</strong>. This is stronger than FOR SHARE \u2014 it blocks both other writers AND other FOR UPDATE/FOR SHARE readers.' },
                { txA: null, txB: { sql: 'BEGIN;' }, lockInfo: '<span class="info-label">Row Locks</span><span class="lock-held">A: FOR UPDATE on (Alice, 1000)</span>', versions: [ v(TX_OLD, true, null, null, [1, 'Alice', 1000], null, false, null, 'lock-a') ], explanation: 'Transaction B begins. It also wants to decrement Alice\'s balance by 100.' },
                { txA: null, txB: { sql: "SELECT balance FROM accounts\n  WHERE name = 'Alice'\n  FOR UPDATE;", result: 'BLOCKED \u2014 waiting for A\'s lock', resultType: 'blocked' }, lockInfo: '<span class="info-label">Row Locks</span><span class="lock-held">A: FOR UPDATE on (Alice, 1000)</span><br><span class="lock-waiting">B: waiting for FOR UPDATE on Alice (blocked by A)</span>', versions: [ v(TX_OLD, true, null, null, [1, 'Alice', 1000], null, false, null, 'lock-a') ], explanation: 'B tries <code>SELECT ... FOR UPDATE</code> on the same row. A already holds the lock. <strong>B is blocked.</strong>' },
                { txA: { sql: "UPDATE accounts\n  SET balance = 900\n  WHERE name = 'Alice';", result: 'UPDATE 1', resultType: 'ok' }, txB: null, lockInfo: '<span class="info-label">Row Locks</span><span class="lock-held">A: FOR UPDATE on Alice (updating)</span><br><span class="lock-waiting">B: still waiting</span>', versions: [ v(TX_OLD, true, TX_A, false, [1, 'Alice', 1000], null, false, null, null), v(TX_A, false, null, null, [1, 'Alice', 900], null, false, null, 'lock-a') ], explanation: 'A decrements: 1000 \u2212 100 = 900. A new version is created. B is still waiting.' },
                { txA: { sql: 'COMMIT;' }, txB: null, lockInfo: '<span class="info-label">Row Locks</span><span class="lock-released">A: lock released</span><br><span class="lock-held">B: unblocked \u2014 lock acquired, re-evaluates query</span>', versions: [ v(TX_OLD, true, TX_A, true, [1, 'Alice', 1000], null, true), v(TX_A, true, null, null, [1, 'Alice', 900]) ], explanation: 'A commits. Lock released. B is unblocked. Crucially, in Read Committed, <strong>B\'s SELECT re-evaluates against the latest committed data</strong> \u2014 it doesn\'t just use the old value.' },
                { txA: null, txB: { sql: '(SELECT resumes \u2014 re-evaluates)', result: '900', resultType: 'warn' }, lockInfo: '<span class="info-label">Row Locks</span><span class="lock-held">B: FOR UPDATE on (Alice, 900)</span>', versions: [ v(TX_OLD, true, TX_A, true, [1, 'Alice', 1000], null, true), v(TX_A, true, null, null, [1, 'Alice', 900], 'B', false, null, 'lock-b') ], explanation: 'B\'s <code>SELECT FOR UPDATE</code> completes. Because this is Read Committed, PostgreSQL <strong>re-checks the row</strong> after unblocking: it sees the new committed version (balance = 900), not the old one. B now correctly knows the balance is 900.' },
                { txA: null, txB: { sql: "UPDATE accounts\n  SET balance = 800\n  WHERE name = 'Alice';", result: 'UPDATE 1', resultType: 'ok' }, lockInfo: '<span class="info-label">Row Locks</span><span class="lock-held">B: FOR UPDATE on Alice (updating)</span>', versions: [ v(TX_OLD, true, TX_A, true, [1, 'Alice', 1000], null, true), v(TX_A, true, TX_B, false, [1, 'Alice', 900]), v(TX_B, false, null, null, [1, 'Alice', 800], null, false, null, 'lock-b') ], explanation: 'B decrements: 900 \u2212 100 = 800. Both decrements are applied correctly.' },
                { txA: null, txB: { sql: 'COMMIT;' }, lockInfo: '<span class="info-label">Row Locks</span><span class="lock-released">All locks released.</span>', versions: [ v(TX_OLD, true, TX_A, true, [1, 'Alice', 1000], null, true), v(TX_A, true, TX_B, true, [1, 'Alice', 900], null, true), v(TX_B, true, null, null, [1, 'Alice', 800]) ], explanation: '<span class="highlight-ok">Final balance: 800.</span> Both decrements applied: 1000 \u2212 100 \u2212 100 = 800. No lost update. Three MVCC versions on disk show the full history. The key: <code>FOR UPDATE</code> serialized the read-then-write pattern, and Read Committed\'s re-evaluation ensured B saw A\'s committed changes.' }
            ]
        },
        {
            id: 'for-update-write-skew', name: 'FOR UPDATE vs Write Skew', tableName: 'doctors',
            txAId: TX_A, txBId: TX_B, columns: ['id', 'name', 'on_call'],
            steps: [
                { txA: { sql: 'BEGIN;' }, txB: null, lockInfo: null, versions: [ v(TX_OLD, true, null, null, [1, 'Alice', 'true']), v(TX_OLD, true, null, null, [2, 'Bob', 'true']) ], explanation: 'The doctors scenario: at least one must remain on call. Under plain Read Committed or Repeatable Read, both doctors can go off call (write skew). <code>FOR UPDATE</code> can prevent this even in Read Committed.' },
                { txA: { sql: "SELECT * FROM doctors\n  WHERE on_call = true\n  FOR UPDATE;", result: '2 rows', resultType: 'ok' }, txB: null, lockInfo: '<span class="info-label">Row Locks</span><span class="lock-held">A: FOR UPDATE on (Alice, true)</span><br><span class="lock-held">A: FOR UPDATE on (Bob, true)</span><br>Both on-call rows are locked. No one can modify them.', versions: [ v(TX_OLD, true, null, null, [1, 'Alice', 'true'], 'A', false, null, 'lock-a'), v(TX_OLD, true, null, null, [2, 'Bob', 'true'], 'A', false, null, 'lock-a') ], explanation: 'A reads all on-call doctors <code>FOR UPDATE</code>, locking <strong>both rows</strong>. This is the key difference \u2014 A locks the entire set it\'s making a decision about, not just the row it will modify.' },
                { txA: null, txB: { sql: 'BEGIN;' }, lockInfo: '<span class="info-label">Row Locks</span><span class="lock-held">A: FOR UPDATE on Alice, Bob</span>', versions: [ v(TX_OLD, true, null, null, [1, 'Alice', 'true'], null, false, null, 'lock-a'), v(TX_OLD, true, null, null, [2, 'Bob', 'true'], null, false, null, 'lock-a') ], explanation: 'Transaction B begins. Bob wants to go off call.' },
                { txA: null, txB: { sql: "SELECT * FROM doctors\n  WHERE on_call = true\n  FOR UPDATE;", result: 'BLOCKED \u2014 waiting for A\'s lock', resultType: 'blocked' }, lockInfo: '<span class="info-label">Row Locks</span><span class="lock-held">A: FOR UPDATE on Alice, Bob</span><br><span class="lock-waiting">B: waiting for FOR UPDATE on on_call=true rows (blocked by A)</span>', versions: [ v(TX_OLD, true, null, null, [1, 'Alice', 'true'], null, false, null, 'lock-a'), v(TX_OLD, true, null, null, [2, 'Bob', 'true'], null, false, null, 'lock-a') ], explanation: 'B also tries to <code>SELECT ... WHERE on_call = true FOR UPDATE</code>. Both matching rows are locked by A. <strong>B is blocked.</strong> B must wait until A releases the locks.' },
                { txA: { sql: "UPDATE doctors SET on_call = false\n  WHERE name = 'Alice';", result: 'UPDATE 1', resultType: 'ok' }, txB: null, lockInfo: '<span class="info-label">Row Locks</span><span class="lock-held">A: FOR UPDATE on Alice (updating), Bob</span><br><span class="lock-waiting">B: still waiting</span>', versions: [ v(TX_OLD, true, TX_A, false, [1, 'Alice', 'true'], null, false, null, null), v(TX_A, false, null, null, [1, 'Alice', 'false'], null, false, null, 'lock-a'), v(TX_OLD, true, null, null, [2, 'Bob', 'true'], null, false, null, 'lock-a') ], explanation: 'A checks the count (2), decides it\'s safe, and sets Alice off call. B is still blocked.' },
                { txA: { sql: 'COMMIT;' }, txB: null, lockInfo: '<span class="info-label">Row Locks</span><span class="lock-released">A: locks released</span><br><span class="lock-held">B: unblocked \u2014 re-evaluates WHERE on_call = true</span>', versions: [ v(TX_OLD, true, TX_A, true, [1, 'Alice', 'true'], null, true), v(TX_A, true, null, null, [1, 'Alice', 'false']), v(TX_OLD, true, null, null, [2, 'Bob', 'true']) ], explanation: 'A commits. Alice is off call. Locks released. B is unblocked and <strong>re-evaluates the WHERE clause</strong> against the latest committed data.' },
                { txA: null, txB: { sql: '(SELECT resumes \u2014 re-evaluates WHERE)', result: '1 row (Bob)', resultType: 'warn' }, lockInfo: '<span class="info-label">Row Locks</span><span class="lock-held">B: FOR UPDATE on (Bob, true)</span><br>Alice no longer matches <code>on_call = true</code> \u2014 skipped.', versions: [ v(TX_OLD, true, TX_A, true, [1, 'Alice', 'true'], null, true), v(TX_A, true, null, null, [1, 'Alice', 'false']), v(TX_OLD, true, null, null, [2, 'Bob', 'true'], 'B', false, null, 'lock-b') ], explanation: 'B\'s query re-evaluates. Alice now has <code>on_call = false</code> \u2014 she no longer matches the WHERE clause and is <strong>skipped</strong>. B only gets Bob. <strong>Count = 1.</strong> B knows it\'s not safe to go off call!' },
                { txA: null, txB: { sql: 'COMMIT;\n-- (no update made)', result: 'Bob stays on call', resultType: 'ok' }, lockInfo: '<span class="info-label">Row Locks</span><span class="lock-released">All locks released.</span>', versions: [ v(TX_OLD, true, TX_A, true, [1, 'Alice', 'true'], null, true), v(TX_A, true, null, null, [1, 'Alice', 'false']), v(TX_OLD, true, null, null, [2, 'Bob', 'true']) ], explanation: '<span class="highlight-ok">Write skew prevented!</span> B saw only 1 doctor on call and chose not to go off call. Final state: Alice off, Bob on. The constraint is preserved. The combination of <code>FOR UPDATE</code> (which locks the decision set) and Read Committed\'s <strong>re-evaluation after unblocking</strong> gives us write skew prevention without needing Serializable isolation.' }
            ]
        }
    ];

    var state = { scenarioIdx: 0, step: 0 };
    function cur() { return scenarios[state.scenarioIdx]; }
    function txidClass(t) { return t === TX_A ? 'tx-a-color' : t === TX_B ? 'tx-b-color' : 'tx-old'; }

    function renderTabs() {
        var c = document.getElementById('lk-tabs'); c.innerHTML = '';
        scenarios.forEach(function(s, i) {
            var b = document.createElement('button');
            b.className = 'tab' + (i === state.scenarioIdx ? ' active' : '');
            b.textContent = s.name;
            b.addEventListener('click', function() { state.scenarioIdx = i; state.step = 0; render(); });
            c.appendChild(b);
        });
    }

    function renderHeaders() {
        var s = cur();
        document.getElementById('lk-header-a').innerHTML = 'Transaction A <span class="txid">txid ' + s.txAId + '</span>';
        document.getElementById('lk-header-b').innerHTML = 'Transaction B <span class="txid">txid ' + s.txBId + '</span>';
    }

    function renderTimelines() {
        var s = cur();
        var aC = document.getElementById('lk-timeline-a'); aC.innerHTML = '';
        var bC = document.getElementById('lk-timeline-b'); bC.innerHTML = '';
        s.steps.forEach(function(sd, idx) {
            function mkCard(tx, side) {
                var card = document.createElement('div');
                if (tx) {
                    card.className = 'step-card';
                    if (idx < state.step) card.className += ' past';
                    else if (idx === state.step) card.className += ' current-' + side;
                    else card.className += ' future';
                    var sql = document.createElement('div'); sql.className = 'sql'; sql.textContent = tx.sql; card.appendChild(sql);
                    if (tx.result && idx <= state.step) {
                        var r = document.createElement('div'); r.className = 'result result-' + tx.resultType; r.textContent = '\u2192 ' + tx.result; card.appendChild(r);
                    }
                } else {
                    card.className = idx <= state.step ? 'step-card idle' : 'step-card future';
                    if (idx <= state.step) card.textContent = '\u2014';
                }
                return card;
            }
            aC.appendChild(mkCard(sd.txA, 'a'));
            bC.appendChild(mkCard(sd.txB, 'b'));
        });
    }

    function renderLockInfo() {
        var sd = cur().steps[state.step];
        var el = document.getElementById('lk-lock-info');
        if (sd.lockInfo) { el.innerHTML = sd.lockInfo; el.className = 'lock-info visible'; }
        else { el.className = 'lock-info'; el.innerHTML = ''; }
    }

    function renderTable() {
        var s = cur(), sd = s.steps[state.step];
        document.getElementById('lk-db-label').innerHTML = s.tableName + ' <span>\u2014 MVCC row versions on disk</span>';
        var table = document.getElementById('lk-db-table'); table.innerHTML = '';
        var thead = document.createElement('thead'), hr = document.createElement('tr');
        ['xmin','xmax'].forEach(function(c){ var th=document.createElement('th'); th.className='mvcc-col'; th.textContent=c; hr.appendChild(th); });
        s.columns.forEach(function(c){ var th=document.createElement('th'); th.textContent=c; hr.appendChild(th); });
        var thV=document.createElement('th'); thV.className='mvcc-col'; thV.textContent=''; hr.appendChild(thV);
        thead.appendChild(hr); table.appendChild(thead);
        var tbody = document.createElement('tbody');
        sd.versions.forEach(function(ver) {
            var tr = document.createElement('tr'), cls = [];
            if (ver.dead) cls.push('version-dead');
            if (ver.seenBy === 'A') cls.push('version-seen-a');
            if (ver.seenBy === 'B') cls.push('version-seen-b');
            if (!ver.xminCommitted) cls.push('version-uncommitted');
            tr.className = cls.join(' ');
            var tdm = document.createElement('td'); tdm.className = 'mvcc-cell';
            var chip = document.createElement('span'); chip.className = 'txid-chip ' + txidClass(ver.xmin); chip.textContent = ver.xmin; tdm.appendChild(chip);
            if (ver.xminCommitted) { var m=document.createElement('span'); m.className='committed-mark'; m.textContent=' \u2714'; tdm.appendChild(m); }
            else { var m=document.createElement('span'); m.className='uncommitted-mark'; m.textContent=' pending'; tdm.appendChild(m); }
            tr.appendChild(tdm);
            var tdx = document.createElement('td'); tdx.className = 'mvcc-cell';
            if (ver.xmax !== null) {
                var cx=document.createElement('span'); cx.className='txid-chip '+txidClass(ver.xmax); cx.textContent=ver.xmax; tdx.appendChild(cx);
                if (ver.xmaxCommitted) { var mx=document.createElement('span'); mx.className='committed-mark'; mx.textContent=' \u2714'; tdx.appendChild(mx); }
                else { var mx=document.createElement('span'); mx.className='uncommitted-mark'; mx.textContent=' pending'; tdx.appendChild(mx); }
            } else { var em=document.createElement('span'); em.className='xmax-empty'; em.textContent='\u2014'; tdx.appendChild(em); }
            tr.appendChild(tdx);
            ver.data.forEach(function(val){ var td=document.createElement('td'); td.textContent=val; tr.appendChild(td); });
            var tdv = document.createElement('td'); tdv.className = 'mvcc-cell';
            if (ver.seenBy) { var badge=document.createElement('span'); badge.className='seen-badge seen-badge-'+ver.seenBy.toLowerCase(); badge.textContent='\u2190 '+ver.seenBy+' reads'; tdv.appendChild(badge); }
            if (ver.lock) {
                var lb=document.createElement('span');
                if (ver.lock === 'lock-a') { lb.className='lock-badge'; lb.textContent='\uD83D\uDD12 A'; }
                else if (ver.lock === 'lock-b') { lb.className='lock-badge'; lb.textContent='\uD83D\uDD12 B'; }
                else if (ver.lock === 'waiting-b') { lb.className='lock-badge lock-badge-waiting'; lb.textContent='\u23f3 B'; }
                tdv.appendChild(lb);
            }
            if (ver.note) { var noteEl=document.createElement('span'); noteEl.className='version-note'; noteEl.textContent=ver.note; tdv.appendChild(noteEl); }
            tr.appendChild(tdv); tbody.appendChild(tr);
        });
        table.appendChild(tbody);
    }

    function renderNav() {
        var total = cur().steps.length;
        document.getElementById('lk-btn-back').disabled = state.step === 0;
        document.getElementById('lk-btn-fwd').disabled = state.step === total - 1;
        document.getElementById('lk-step-indicator').textContent = 'Step ' + (state.step + 1) + ' of ' + total;
    }

    function render() {
        renderTabs(); renderHeaders(); renderTimelines(); renderLockInfo(); renderTable();
        document.getElementById('lk-explanation').innerHTML = cur().steps[state.step].explanation;
        renderNav();
    }

    document.getElementById('lk-btn-back').addEventListener('click', function() { if (state.step > 0) { state.step--; render(); } });
    document.getElementById('lk-btn-fwd').addEventListener('click', function() { if (state.step < cur().steps.length - 1) { state.step++; render(); } });

    var demo = document.getElementById('lk-demo');
    demo.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowLeft' && state.step > 0) { state.step--; render(); }
        if (e.key === 'ArrowRight' && state.step < cur().steps.length - 1) { state.step++; render(); }
    });
    demo.setAttribute('tabindex', '0');

    render();
})();
</script>

# Thanks and further reading

The inspiration for building an interactive simulator came from the [TheOtherBrian1](https://github.com/TheOtherBrian1) excellent site [“Postgres Locks Explained”](https://postgreslocksexplained.com/).

PostgreSQL documentation on isolation levels and locking:

- [https://www.postgresql.org/docs/current/transaction-iso.html](https://www.postgresql.org/docs/current/transaction-iso.html)
- [https://www.postgresql.org/docs/current/explicit-locking.html](https://www.postgresql.org/docs/current/explicit-locking.html)

AI tools (Gemini, ChatGPT) were used to improve grammar and clarity of the text. The interactive simulators were built with the help of Claude Code.
