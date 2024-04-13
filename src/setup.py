import sys
import re
import os

def is_patched(file_path: str) -> bool:
    try:
        with open(file_path, "r") as f:
            content = f.read()
            if "/*Patched By NayutaTeam*/" in content:
                return True
    except FileNotFoundError:
        pass
    return False

def patch_driver(path: str):
    try:
        # patch driver
        print(f'[PATCH] patching driver for "{path}"', file=sys.stderr)

        def replace(path: str, old_str: str, new_str: str):
            try:
                with open(path, "r") as f:
                    content = f.read()
                content = content.replace(old_str, new_str)
                with open(path, "w") as f:
                    f.write(content)
                print(f'Patch applied to {path}')
            except Exception as e:
                print(f'Error patching {path}: {e}', file=sys.stderr)

        server_path = os.path.join(path, "package", "lib", "server")
        chromium_path = os.path.join(server_path, "chromium")

        # comment out all "Runtime.enable" occurrences
        cr_devtools_path = os.path.join(chromium_path, "crDevTools.js")
        if not is_patched(cr_devtools_path):
            replace(cr_devtools_path, "session.send('Runtime.enable'),", "/*session.send('Runtime.enable'), */")

        cr_page_path = os.path.join(chromium_path, "crPage.js")
        if not is_patched(cr_page_path):
            with open(cr_page_path, "r") as f:
                cr_page = f.read()
                cr_page = cr_page.replace("this._client.send('Runtime.enable', {}),",
                                          "/*this._client.send('Runtime.enable', {}),*/")
                cr_page = cr_page.replace("session._sendMayFail('Runtime.enable');",
                                          "/*session._sendMayFail('Runtime.enable');*/")
            with open(cr_page_path, "w") as f:
                f.write(cr_page)
            print(f'Patch applied to {cr_page_path}')

        cr_sv_worker_path = os.path.join(chromium_path, "crServiceWorker.js")
        if not is_patched(cr_sv_worker_path):
            replace(cr_sv_worker_path, "session.send('Runtime.enable', {}).catch(e => {});",
                    "/*session.send('Runtime.enable', {}).catch(e => {});*/")

        # patch ExecutionContext eval to still work
        frames_path = os.path.join(server_path, "frames.js")

        _context_re = re.compile(r".*\s_context?\s*\(world\)\s*\{(?:[^}{]+|\{(?:[^}{]+|\{[^}{]*\})*\})*\}")
        _context_replacement = \
            " async _context(world) {\n" \
            """
            // atm ignores world_name
            if (this._isolatedContext == undefined) {
              var worldName = "utility"
              var result = await this._page._delegate._mainFrameSession._client.send('Page.createIsolatedWorld', {
                frameId: this._id,
                grantUniveralAccess: true,
                worldName: worldName
              });
              var crContext = new _crExecutionContext.CRExecutionContext(this._page._delegate._mainFrameSession._client, {id:result.executionContextId})
              this._isolatedContext = new _dom.FrameExecutionContext(crContext, this, worldName)
            }
            return this._isolatedContext
            \n""" \
            "}"
        clear_re = re.compile(
            r".\s_onClearLifecycle?\s*\(\)\s*\{")
        clear_repl = \
            " _onClearLifecycle() {\n" \
            """
            this._isolatedContext = undefined;
            """

        if not is_patched(frames_path):
            with open(frames_path, "r") as f:
                frames_js = f.read()
                frames_js = "var _crExecutionContext = require('./chromium/crExecutionContext')\n" \
                            "var _dom =  require('./dom')\n" \
                            + "\n" + frames_js

                # patch _context function
                frames_js = _context_re.subn(_context_replacement, frames_js, count=1)[0]
                frames_js = clear_re.subn(clear_repl, frames_js, count=1)[0]

            with open(frames_path, "w") as f:
                f.write(frames_js)
            print(f'Patch applied to {frames_path}')

        # Add patch marker to patched files
        for patched_file in [cr_devtools_path, cr_page_path, cr_sv_worker_path, frames_path]:
            if not is_patched(patched_file):
                with open(patched_file, "a") as f:
                    f.write("\n/*Patched By NayutaTeam*/")
                    print(f'Patch marker added to {patched_file}')

    except Exception as e:
        print(f'Error: {e}', file=sys.stderr)

def main(path: str = ""):
    try:
        if not path:
            path = ".\\.playwright"
        if not os.path.exists(path):
            print(f"Error: Path '{path}' does not exist.")
            return
        patch_driver(path)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = ".\\.playwright"
    main(path)