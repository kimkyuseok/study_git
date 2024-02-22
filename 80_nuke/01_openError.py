import sgtk

tk = sgtk.sgtk_from_path( f'V:\VFX\FSH' )   ## 프로젝트 루트 경로
unreg_cmd = sgtk.get_command('unregister_folders', tk)

params = {"path": "V:\VFX\FSH\shot\e104\e104_s022_0100"}   ## 언레지스트 할 대상 경로
#params = {"entity": {"type":"Asset", "id":1226} }  ## 또는 언레지스트 할 엔티티 정보
print( unreg_cmd.execute(params) )
