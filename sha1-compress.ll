; ModuleID = '<stdin>'
source_filename = "sha1-arm-unrolled.cpp"
target datalayout = "e-m:o-i64:64-i128:128-n32:64-S128-Fn32"
target triple = "arm64-apple-macosx14.0.0"

; Function Attrs: mustprogress nofree noinline norecurse nosync nounwind ssp willreturn memory(argmem: readwrite)
define hidden fastcc void @_ZL26sha1_arm_unrolled_compressILm1EEvPjPKh(ptr nocapture noundef %0, ptr nocapture noundef readonly %1) unnamed_addr #0 {
  %3 = load <4 x i32>, ptr %0, align 4
  %4 = getelementptr inbounds i8, ptr %0, i64 16
  %5 = load i32, ptr %4, align 4, !tbaa !4
  %6 = load <16 x i8>, ptr %1, align 1
  %7 = shufflevector <16 x i8> %6, <16 x i8> poison, <16 x i32> <i32 3, i32 2, i32 1, i32 0, i32 7, i32 6, i32 5, i32 4, i32 11, i32 10, i32 9, i32 8, i32 15, i32 14, i32 13, i32 12>
  %8 = bitcast <16 x i8> %7 to <4 x i32>
  %9 = getelementptr inbounds i8, ptr %1, i64 16
  %10 = load <16 x i8>, ptr %9, align 1
  %11 = shufflevector <16 x i8> %10, <16 x i8> poison, <16 x i32> <i32 3, i32 2, i32 1, i32 0, i32 7, i32 6, i32 5, i32 4, i32 11, i32 10, i32 9, i32 8, i32 15, i32 14, i32 13, i32 12>
  %12 = bitcast <16 x i8> %11 to <4 x i32>
  %13 = getelementptr inbounds i8, ptr %1, i64 32
  %14 = load <16 x i8>, ptr %13, align 1
  %15 = shufflevector <16 x i8> %14, <16 x i8> poison, <16 x i32> <i32 3, i32 2, i32 1, i32 0, i32 7, i32 6, i32 5, i32 4, i32 11, i32 10, i32 9, i32 8, i32 15, i32 14, i32 13, i32 12>
  %16 = bitcast <16 x i8> %15 to <4 x i32>
  %17 = getelementptr inbounds i8, ptr %1, i64 48
  %18 = load <16 x i8>, ptr %17, align 1
  %19 = shufflevector <16 x i8> %18, <16 x i8> poison, <16 x i32> <i32 3, i32 2, i32 1, i32 0, i32 7, i32 6, i32 5, i32 4, i32 11, i32 10, i32 9, i32 8, i32 15, i32 14, i32 13, i32 12>
  %20 = bitcast <16 x i8> %19 to <4 x i32>
  %21 = add <4 x i32> %8, <i32 1518500249, i32 1518500249, i32 1518500249, i32 1518500249>
  %22 = add <4 x i32> %12, <i32 1518500249, i32 1518500249, i32 1518500249, i32 1518500249>
  %23 = add <4 x i32> %16, <i32 1518500249, i32 1518500249, i32 1518500249, i32 1518500249>
  %24 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %8, <4 x i32> %12, <4 x i32> %16)
  %25 = add <4 x i32> %20, <i32 1518500249, i32 1518500249, i32 1518500249, i32 1518500249>
  %26 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %24, <4 x i32> %20)
  %27 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %12, <4 x i32> %16, <4 x i32> %20)
  %28 = add <4 x i32> %26, <i32 1518500249, i32 1518500249, i32 1518500249, i32 1518500249>
  %29 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %27, <4 x i32> %26)
  %30 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %16, <4 x i32> %20, <4 x i32> %26)
  %31 = add <4 x i32> %29, <i32 1859775393, i32 1859775393, i32 1859775393, i32 1859775393>
  %32 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %30, <4 x i32> %29)
  %33 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %20, <4 x i32> %26, <4 x i32> %29)
  %34 = add <4 x i32> %32, <i32 1859775393, i32 1859775393, i32 1859775393, i32 1859775393>
  %35 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %33, <4 x i32> %32)
  %36 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %26, <4 x i32> %29, <4 x i32> %32)
  %37 = add <4 x i32> %35, <i32 1859775393, i32 1859775393, i32 1859775393, i32 1859775393>
  %38 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %36, <4 x i32> %35)
  %39 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %29, <4 x i32> %32, <4 x i32> %35)
  %40 = add <4 x i32> %38, <i32 1859775393, i32 1859775393, i32 1859775393, i32 1859775393>
  %41 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %39, <4 x i32> %38)
  %42 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %32, <4 x i32> %35, <4 x i32> %38)
  %43 = add <4 x i32> %41, <i32 1859775393, i32 1859775393, i32 1859775393, i32 1859775393>
  %44 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %42, <4 x i32> %41)
  %45 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %35, <4 x i32> %38, <4 x i32> %41)
  %46 = add <4 x i32> %44, <i32 -1894007588, i32 -1894007588, i32 -1894007588, i32 -1894007588>
  %47 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %45, <4 x i32> %44)
  %48 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %38, <4 x i32> %41, <4 x i32> %44)
  %49 = add <4 x i32> %47, <i32 -1894007588, i32 -1894007588, i32 -1894007588, i32 -1894007588>
  %50 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %48, <4 x i32> %47)
  %51 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %41, <4 x i32> %44, <4 x i32> %47)
  %52 = add <4 x i32> %50, <i32 -1894007588, i32 -1894007588, i32 -1894007588, i32 -1894007588>
  %53 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %51, <4 x i32> %50)
  %54 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %44, <4 x i32> %47, <4 x i32> %50)
  %55 = add <4 x i32> %53, <i32 -1894007588, i32 -1894007588, i32 -1894007588, i32 -1894007588>
  %56 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %54, <4 x i32> %53)
  %57 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %47, <4 x i32> %50, <4 x i32> %53)
  %58 = add <4 x i32> %56, <i32 -1894007588, i32 -1894007588, i32 -1894007588, i32 -1894007588>
  %59 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %57, <4 x i32> %56)
  %60 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %50, <4 x i32> %53, <4 x i32> %56)
  %61 = add <4 x i32> %59, <i32 -899497514, i32 -899497514, i32 -899497514, i32 -899497514>
  %62 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %60, <4 x i32> %59)
  %63 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %53, <4 x i32> %56, <4 x i32> %59)
  %64 = add <4 x i32> %62, <i32 -899497514, i32 -899497514, i32 -899497514, i32 -899497514>
  %65 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %63, <4 x i32> %62)
  %66 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %56, <4 x i32> %59, <4 x i32> %62)
  %67 = add <4 x i32> %65, <i32 -899497514, i32 -899497514, i32 -899497514, i32 -899497514>
  %68 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %66, <4 x i32> %65)
  %69 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %59, <4 x i32> %62, <4 x i32> %65)
  %70 = add <4 x i32> %68, <i32 -899497514, i32 -899497514, i32 -899497514, i32 -899497514>
  %71 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %69, <4 x i32> %68)
  %72 = add <4 x i32> %71, <i32 -899497514, i32 -899497514, i32 -899497514, i32 -899497514>
  %73 = extractelement <4 x i32> %3, i64 0
  %74 = tail call noundef i32 @llvm.aarch64.crypto.sha1h(i32 %73)
  %75 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1c(<4 x i32> %3, i32 %5, <4 x i32> %21)
  %76 = extractelement <4 x i32> %75, i64 0
  %77 = tail call noundef i32 @llvm.aarch64.crypto.sha1h(i32 %76)
  %78 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1c(<4 x i32> %75, i32 %74, <4 x i32> %22)
  %79 = extractelement <4 x i32> %78, i64 0
  %80 = tail call noundef i32 @llvm.aarch64.crypto.sha1h(i32 %79)
  %81 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1c(<4 x i32> %78, i32 %77, <4 x i32> %23)
  %82 = extractelement <4 x i32> %81, i64 0
  %83 = tail call noundef i32 @llvm.aarch64.crypto.sha1h(i32 %82)
  %84 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1c(<4 x i32> %81, i32 %80, <4 x i32> %25)
  %85 = extractelement <4 x i32> %84, i64 0
  %86 = tail call noundef i32 @llvm.aarch64.crypto.sha1h(i32 %85)
  %87 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1c(<4 x i32> %84, i32 %83, <4 x i32> %28)
  %88 = extractelement <4 x i32> %87, i64 0
  %89 = tail call noundef i32 @llvm.aarch64.crypto.sha1h(i32 %88)
  %90 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %87, i32 %86, <4 x i32> %31)
  %91 = extractelement <4 x i32> %90, i64 0
  %92 = tail call noundef i32 @llvm.aarch64.crypto.sha1h(i32 %91)
  %93 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %90, i32 %89, <4 x i32> %34)
  %94 = extractelement <4 x i32> %93, i64 0
  %95 = tail call noundef i32 @llvm.aarch64.crypto.sha1h(i32 %94)
  %96 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %93, i32 %92, <4 x i32> %37)
  %97 = extractelement <4 x i32> %96, i64 0
  %98 = tail call noundef i32 @llvm.aarch64.crypto.sha1h(i32 %97)
  %99 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %96, i32 %95, <4 x i32> %40)
  %100 = extractelement <4 x i32> %99, i64 0
  %101 = tail call noundef i32 @llvm.aarch64.crypto.sha1h(i32 %100)
  %102 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %99, i32 %98, <4 x i32> %43)
  %103 = extractelement <4 x i32> %102, i64 0
  %104 = tail call noundef i32 @llvm.aarch64.crypto.sha1h(i32 %103)
  %105 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1m(<4 x i32> %102, i32 %101, <4 x i32> %46)
  %106 = extractelement <4 x i32> %105, i64 0
  %107 = tail call noundef i32 @llvm.aarch64.crypto.sha1h(i32 %106)
  %108 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1m(<4 x i32> %105, i32 %104, <4 x i32> %49)
  %109 = extractelement <4 x i32> %108, i64 0
  %110 = tail call noundef i32 @llvm.aarch64.crypto.sha1h(i32 %109)
  %111 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1m(<4 x i32> %108, i32 %107, <4 x i32> %52)
  %112 = extractelement <4 x i32> %111, i64 0
  %113 = tail call noundef i32 @llvm.aarch64.crypto.sha1h(i32 %112)
  %114 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1m(<4 x i32> %111, i32 %110, <4 x i32> %55)
  %115 = extractelement <4 x i32> %114, i64 0
  %116 = tail call noundef i32 @llvm.aarch64.crypto.sha1h(i32 %115)
  %117 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1m(<4 x i32> %114, i32 %113, <4 x i32> %58)
  %118 = extractelement <4 x i32> %117, i64 0
  %119 = tail call noundef i32 @llvm.aarch64.crypto.sha1h(i32 %118)
  %120 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %117, i32 %116, <4 x i32> %61)
  %121 = extractelement <4 x i32> %120, i64 0
  %122 = tail call noundef i32 @llvm.aarch64.crypto.sha1h(i32 %121)
  %123 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %120, i32 %119, <4 x i32> %64)
  %124 = extractelement <4 x i32> %123, i64 0
  %125 = tail call noundef i32 @llvm.aarch64.crypto.sha1h(i32 %124)
  %126 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %123, i32 %122, <4 x i32> %67)
  %127 = extractelement <4 x i32> %126, i64 0
  %128 = tail call noundef i32 @llvm.aarch64.crypto.sha1h(i32 %127)
  %129 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %126, i32 %125, <4 x i32> %70)
  %130 = extractelement <4 x i32> %129, i64 0
  %131 = tail call noundef i32 @llvm.aarch64.crypto.sha1h(i32 %130)
  %132 = tail call noundef <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %129, i32 %128, <4 x i32> %72)
  %133 = add <4 x i32> %132, %3
  %134 = add i32 %131, %5
  store <4 x i32> %133, ptr %0, align 4
  store i32 %134, ptr %4, align 4, !tbaa !4
  ret void
}

; Function Attrs: nocallback nofree nosync nounwind willreturn memory(none)
declare i32 @llvm.aarch64.crypto.sha1h(i32) #1

; Function Attrs: nocallback nofree nosync nounwind willreturn memory(none)
declare <4 x i32> @llvm.aarch64.crypto.sha1c(<4 x i32>, i32, <4 x i32>) #1

; Function Attrs: nocallback nofree nosync nounwind willreturn memory(none)
declare <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32>, <4 x i32>, <4 x i32>) #1

; Function Attrs: nocallback nofree nosync nounwind willreturn memory(none)
declare <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32>, <4 x i32>) #1

; Function Attrs: nocallback nofree nosync nounwind willreturn memory(none)
declare <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32>, i32, <4 x i32>) #1

; Function Attrs: nocallback nofree nosync nounwind willreturn memory(none)
declare <4 x i32> @llvm.aarch64.crypto.sha1m(<4 x i32>, i32, <4 x i32>) #1

attributes #0 = { mustprogress nofree noinline norecurse nosync nounwind ssp willreturn memory(argmem: readwrite) "frame-pointer"="non-leaf" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="apple-a14" "target-features"="+aes,+altnzcv,+ccdp,+ccidx,+complxnum,+crc,+dit,+dotprod,+flagm,+fp-armv8,+fp16fml,+fptoint,+fullfp16,+jsconv,+lse,+neon,+pauth,+perfmon,+predres,+ras,+rcpc,+rdm,+sb,+sha2,+sha3,+specrestrict,+ssbs,+v8.1a,+v8.2a,+v8.3a,+v8.4a,+v8a,+zcm,+zcz" }
attributes #1 = { nocallback nofree nosync nounwind willreturn memory(none) }

!llvm.linker.options = !{}
!llvm.module.flags = !{!0, !1, !2}
!llvm.ident = !{!3}

!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{i32 8, !"PIC Level", i32 2}
!2 = !{i32 7, !"frame-pointer", i32 1}
!3 = !{!"Homebrew clang version 19.1.5"}
!4 = !{!5, !5, i64 0}
!5 = !{!"int", !6, i64 0}
!6 = !{!"omnipotent char", !7, i64 0}
!7 = !{!"Simple C++ TBAA"}
