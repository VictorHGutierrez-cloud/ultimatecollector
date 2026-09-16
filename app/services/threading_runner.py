#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Executa SandboxRunner em thread separada para a UI não travar."""

from __future__ import annotations

import threading
from typing import Callable, Optional

LogFn = Callable[[str], None]
DoneFn = Callable[[int], None]


class ThreadingRunner:
    def __init__(self) -> None:
        self._busy = False
        self._lock = threading.Lock()

    @property
    def busy(self) -> bool:
        return self._busy

    def run(
        self,
        target: Callable[[], int],
        on_done: Optional[DoneFn] = None,
        on_error: Optional[Callable[[Exception], None]] = None,
    ) -> bool:
        with self._lock:
            if self._busy:
                return False
            self._busy = True

        def _worker() -> None:
            code = 1
            try:
                code = int(target())
            except Exception as exc:
                if on_error:
                    on_error(exc)
                else:
                    raise
            finally:
                with self._lock:
                    self._busy = False
                if on_done:
                    on_done(code)

        threading.Thread(target=_worker, daemon=True).start()
        return True
