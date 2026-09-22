<!--
  CastleFrame — wraps page content in a pixel-art castle, standing in a
  landscape (sky, distant hills, grass) that stretches the full width of
  whatever container this is placed in.

  THIS FILE IS LAYOUT ONLY. It never names an image file or an image size;
  all of that lives in castle-art.css. To change the artwork, edit that file
  (or just overwrite the PNGs in public/castle/). You should not need to touch
  this file for an art swap.

  Every piece of artwork below is marked  <!-- ART: name -->  so it is easy to
  find. The text of the page goes into the default slot (the parchment panel).
-->
<template>
  <div class="castle-landscape">
    <!-- ART: sky-clouds + sun + hills. Spans the FULL width, behind everything. -->
    <div class="castle-landscape__backdrop" aria-hidden="true">
      <div class="castle-landscape__sun"></div>
      <div class="castle-landscape__hills"></div>
    </div>

    <!-- The castle itself: towers + wall, centred on top of the backdrop. -->
    <div class="castle">
      <!-- LEFT TOWER -->
      <div class="castle__tower castle__tower--left" aria-hidden="true">
        <div class="castle__tower-art">
          <!-- ART: tower-cap -->
          <div class="castle__tower-cap"></div>
          <!-- ART: tower-body (tiles), tower-window, tower-ivy, tower-banner -->
          <div class="castle__tower-body">
            <div class="castle__tower-window castle__tower-window--a"></div>
            <div class="castle__tower-window castle__tower-window--b"></div>
            <div class="castle__tower-window castle__tower-window--c"></div>
            <div class="castle__tower-ivy"></div>
          </div>
          <div class="castle__tower-banner"></div>
        </div>
      </div>

      <!-- CENTRE: the wall, with the page content inside -->
      <div class="castle__wall">
        <!-- ART: wall-top (battlements) -->
        <div class="castle__wall-top" aria-hidden="true"></div>
        <!-- ART: wall-body (tiles) -->
        <div class="castle__wall-body">
          <!-- ART: panel-frame (wooden frame) + parchment (paper) -->
          <div class="castle__panel">
            <slot />
          </div>
          <!-- ART: torch, gate, torch -->
          <div class="castle__gate-row" aria-hidden="true">
            <div class="castle__torch"></div>
            <div class="castle__gate"></div>
            <div class="castle__torch"></div>
          </div>
        </div>
      </div>

      <!-- RIGHT TOWER (same art, mirrored by the CSS) -->
      <div class="castle__tower castle__tower--right" aria-hidden="true">
        <div class="castle__tower-art">
          <div class="castle__tower-cap"></div>
          <div class="castle__tower-body">
            <div class="castle__tower-window castle__tower-window--a"></div>
            <div class="castle__tower-window castle__tower-window--b"></div>
            <div class="castle__tower-window castle__tower-window--c"></div>
            <div class="castle__tower-ivy"></div>
          </div>
          <div class="castle__tower-banner"></div>
        </div>
      </div>
    </div>

    <!-- ART: grass. Spans the FULL width, in front of everything, at the bottom. -->
    <div class="castle-landscape__grass" aria-hidden="true"></div>
  </div>
</template>

<script setup lang="ts">
// All artwork settings (files + sizes) live in this one CSS file.
import './castle-art.css'
</script>

<style>
/* Class names all start with "castle" so nothing here can clash with the rest
   of the site. Sizes are written as (art pixels * --px). */

.castle-landscape {
  /* SIZE OF ONE ART PIXEL ON SCREEN. Keep it a whole number so the pixel art
     stays sharp. Phones do NOT shrink this; they trim the towers instead. */
  --px: 4px;

  --castle-sky-top: #79c4f2;
  --castle-sky-bottom: #cfeefc;
  --castle-tower-visible: var(--castle-tower-visible-phone);
  --castle-wall-pad: 3;    /* stone showing around the panel, in art pixels */
  --castle-panel-pad: 3;   /* space between the frame and the text */
  --castle-max-width: 1000px; /* widest the castle itself ever gets; the
                                  landscape fills whatever space is left over */

  position: relative;
  overflow: hidden;
  isolation: isolate;
  image-rendering: pixelated;
  padding-top: calc(6 * var(--px));
  padding-bottom: calc((var(--art-grass-h) - 4) * var(--px));
}

@media (min-width: 600px) {
  .castle-landscape {
    --castle-tower-visible: var(--castle-tower-visible-tablet);
    --castle-wall-pad: 6;
    --castle-panel-pad: 5;
  }
}
@media (min-width: 960px) {
  .castle-landscape {
    /* Wide screens show the whole tower. */
    --castle-tower-visible: var(--art-tower-body-w);
  }
}

/* ---- Backdrop: sky + hills, full width, behind everything ---------------- */
.castle-landscape__backdrop {
  position: absolute;
  inset: 0;
  z-index: 0;
  background-image:
    var(--art-clouds),
    linear-gradient(to bottom, var(--castle-sky-top), var(--castle-sky-bottom) 70%, #eaf7fd);
  background-repeat: repeat-x, no-repeat;
  background-position: 0 calc(2 * var(--px)), 0 0;
  background-size:
    calc(var(--art-clouds-w) * var(--px)) calc(var(--art-clouds-h) * var(--px)),
    100% 100%;
}
.castle-landscape__hills {
  position: absolute;
  left: 0; right: 0;
  bottom: calc((var(--art-grass-h) - 3) * var(--px)); /* sits just above the grass */
  height: calc(var(--art-hills-h) * var(--px));
  background: var(--art-hills) repeat-x bottom left /
    calc(var(--art-hills-w) * var(--px)) calc(var(--art-hills-h) * var(--px));
}
.castle-landscape__sun {
  display: none;
  position: absolute;
  top: calc(4 * var(--px));
  left: calc(4 * var(--px));
  width: calc(var(--art-sun-w) * var(--px));
  height: calc(var(--art-sun-h) * var(--px));
  background: var(--art-sun) no-repeat 0 0 / 100% 100%;
}
@media (min-width: 960px) {
  .castle-landscape__sun { display: block; }
}

/* ---- Grass: full width, in front of everything, at the very bottom ------- */
.castle-landscape__grass {
  position: absolute;
  left: 0; right: 0; bottom: 0;
  z-index: 3;
  pointer-events: none;
  height: calc(var(--art-grass-h) * var(--px));
  background: var(--art-grass) repeat-x 0 0 /
    calc(var(--art-grass-w) * var(--px)) calc(var(--art-grass-h) * var(--px));
}

/* ---- The castle itself: centred, capped at --castle-max-width ------------ */
.castle {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns:
    calc(var(--castle-tower-visible) * var(--px))
    minmax(0, 1fr)
    calc(var(--castle-tower-visible) * var(--px));
  max-width: var(--castle-max-width);
  margin: 0 auto;
}

/* ---- Towers ------------------------------------------------------------- */
.castle__tower {
  position: relative;
  grid-row: 1;
  overflow: hidden;   /* this is what TRIMS the tower on small screens */
}
.castle__tower--left  { grid-column: 1; }
.castle__tower--right { grid-column: 3; }

/* The tower artwork is always drawn at full size and pinned to the wall side;
   the column above is narrower on small screens, so the outer part is cut off. */
.castle__tower-art {
  position: absolute;
  top: 0;
  bottom: 0;
  width: calc(var(--art-tower-body-w) * var(--px));
}
.castle__tower--left  .castle__tower-art { right: 0; }
.castle__tower--right .castle__tower-art { left: 0; transform: scaleX(-1); }

.castle__tower-cap {
  position: absolute;
  top: 0; left: 0; right: 0;
  height: calc(var(--art-tower-cap-h) * var(--px));
  background: var(--art-tower-cap) no-repeat 0 0 /
    calc(var(--art-tower-cap-w) * var(--px)) calc(var(--art-tower-cap-h) * var(--px));
}
.castle__tower-body {
  position: absolute;
  top: calc(var(--art-tower-cap-h) * var(--px));
  bottom: 0; left: 0; right: 0;
  background: var(--art-tower-body) repeat-y 0 0 /
    calc(var(--art-tower-body-w) * var(--px)) calc(var(--art-tower-body-h) * var(--px));
}
.castle__tower-ivy {
  position: absolute;
  inset: 0;
  background: var(--art-tower-ivy) repeat-y 0 0 /
    calc(var(--art-tower-ivy-w) * var(--px)) calc(var(--art-tower-ivy-h) * var(--px));
}
.castle__tower--right .castle__tower-ivy {
  background-position: 0 calc(24 * var(--px));   /* so the two towers don't look identical */
}

.castle__tower-window {
  display: none;
  position: absolute;
  left: calc(var(--castle-window-x) * var(--px));
  width: calc(var(--art-tower-window-w) * var(--px));
  height: calc(var(--art-tower-window-h) * var(--px));
  background: var(--art-tower-window) no-repeat 0 0 / 100% 100%;
}
.castle__tower-window--a { top: calc(16% - var(--art-tower-window-h) * var(--px) / 2); }
.castle__tower-window--b { top: calc(46% - var(--art-tower-window-h) * var(--px) / 2); }
.castle__tower-window--c { top: calc(76% - var(--art-tower-window-h) * var(--px) / 2); }
@media (min-width: 600px) {
  .castle__tower-window { display: block; }
}

.castle__tower-banner {
  display: none;
  position: absolute;
  top: calc(var(--castle-banner-y) * var(--px));
  left: calc(var(--castle-banner-x) * var(--px));
  width: calc(var(--art-tower-banner-w) * var(--px));
  height: calc(var(--art-tower-banner-h) * var(--px));
  background: var(--art-tower-banner) no-repeat 0 0 / 100% 100%;
}
@media (min-width: 960px) {
  .castle__tower-banner { display: block; }
}

/* ---- Wall ---------------------------------------------------------------- */
.castle__wall {
  grid-column: 2;
  grid-row: 1;
  position: relative;
  display: flex;
  flex-direction: column;
  min-width: 0;
  /* The wall starts lower than the towers so the towers stand above it. */
  margin-top: calc((var(--art-tower-cap-h) - var(--art-wall-top-h)) * var(--px));
}
.castle__wall-top {
  flex: none;
  height: calc(var(--art-wall-top-h) * var(--px));
  background: var(--art-wall-top) repeat-x 0 0 /
    calc(var(--art-wall-top-w) * var(--px)) calc(var(--art-wall-top-h) * var(--px));
}
.castle__wall-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: calc(4 * var(--px)) calc(var(--castle-wall-pad) * var(--px)) calc(2 * var(--px));
  background: var(--art-wall-body) repeat 0 0 /
    calc(var(--art-wall-body-w) * var(--px)) calc(var(--art-wall-body-h) * var(--px));
  /* stepped (not blurry) shadows: under the battlements and beside the towers */
  box-shadow:
    inset 0 calc(2 * var(--px)) 0 rgba(70, 52, 24, 0.28),
    inset calc(2 * var(--px)) 0 0 rgba(70, 52, 24, 0.16),
    inset calc(-2 * var(--px)) 0 0 rgba(70, 52, 24, 0.16);
}

/* ---- The panel that holds the page content ------------------------------ */
.castle__panel {
  position: relative;
  border: calc(var(--art-panel-frame-slice) * var(--px)) solid transparent;
  border-image-source: var(--art-panel-frame);
  border-image-slice: var(--art-panel-frame-slice);
  border-image-width: calc(var(--art-panel-frame-slice) * var(--px));
  border-image-repeat: repeat;
  background: var(--art-parchment) repeat 0 0 /
    calc(var(--art-parchment-w) * var(--px)) calc(var(--art-parchment-h) * var(--px));
  background-clip: padding-box;
  padding: calc(var(--castle-panel-pad) * var(--px));
  color: #3b2a17;
  overflow: hidden;   /* anything too wide is trimmed rather than squashed */
}

/* ---- Gate and torches ---------------------------------------------------- */
.castle__gate-row {
  display: flex;
  justify-content: center;
  align-items: flex-end;
  gap: calc(6 * var(--px));
  margin-top: calc(6 * var(--px));
}
.castle__gate {
  flex: none;
  width: calc(var(--art-gate-w) * var(--px));
  height: calc(var(--art-gate-h) * var(--px));
  background: var(--art-gate) no-repeat 0 0 / 100% 100%;
}
.castle__torch {
  display: none;
  flex: none;
  align-self: flex-start;
  margin-top: calc(10 * var(--px));
  width: calc(var(--art-torch-w) * var(--px));
  height: calc(var(--art-torch-h) * var(--px));
  background: var(--art-torch) no-repeat 0 0 /
    calc(var(--art-torch-w) * var(--art-torch-frames) * var(--px)) calc(var(--art-torch-h) * var(--px));
  animation: castle-torch 0.6s steps(var(--art-torch-frames)) infinite;
}
@media (min-width: 600px) {
  .castle__torch { display: block; }
}
@keyframes castle-torch {
  to { background-position: calc(var(--art-torch-w) * var(--art-torch-frames) * var(--px) * -1) 0; }
}

@media (prefers-reduced-motion: reduce) {
  .castle__torch { animation: none; }
}
</style>
